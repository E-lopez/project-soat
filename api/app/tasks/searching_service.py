from collections import defaultdict
from sqlalchemy import and_, or_, select

from app.schemas.DefinitionsIndex import DefinitionsIndex
from app.schemas.Dto.QueryRequest import QueryRequest
from app.dependencies.session_manager import DbSession
from app.constants.sql_statements import hybrid_query


async def _fetch_definitions(session: DbSession, rows) -> str:
    defs_by_company = defaultdict(set)
    for d in rows:
        if d.definitions:
            defs_by_company[d.company].update(d.definitions)

    unique_defs_by_company = {
        company: list(defs)
        for company, defs in defs_by_company.items()
        if defs
    }

    conditions = [
        and_(DefinitionsIndex.company == company, DefinitionsIndex.key_word.in_(defs))  # type: ignore
        for company, defs in unique_defs_by_company.items()
    ]

    if conditions:
        result = await session.execute(select(DefinitionsIndex).where(or_(*conditions)))
        records = result.scalars().all()
    else:
        records = []

    definitions_list = [
        f"### AIRLINE: {company}\n" + "\n".join(
            f"{r.key_word}: {r.raw_string}" for r in records if r.company == company
        )
        for company in unique_defs_by_company
    ]

    return "\n".join(definitions_list)


async def hybrid_search(session: DbSession, query_embedding: list[float], payload: QueryRequest) -> tuple[str, str, list[str]]:
    company_filter = payload.company or None
    limit = 15 if company_filter is None else 7
    main_res = await session.execute(
        hybrid_query,
        {
            "company": company_filter,
            "embedding": str(query_embedding),
            "query": payload.query,
            "limit": limit
        }
    )
    rows = main_res.all()

    main_list = [
        f"--- START SOURCE DOCUMENT {row.index} ---\n"
        f"Company: {row.company} (Section {row.section})\n"
        f"Rules:\n{row.raw_string}\n"
        f"--- END SOURCE DOCUMENT {row.index} ---"
        for row in rows
    ]
    sources = [row.raw_string for row in rows]

    definitions_string = await _fetch_definitions(session, rows)

    context_string = "=== CONTRACT RULES ===\n" + "\n\n".join(main_list) if main_list else ""

    return context_string, definitions_string, sources
