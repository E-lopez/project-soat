import pathlib
import re

pattern = r'(?=\s*\[Scene:)'

def get_string_to_embed(episode: dict, scene: str, actual_lines: list) -> str:
    return (
        f"Episode: {episode.get('metadata', {}).get('ep_name', 'N/A')}\n"
        f"Writer: {episode.get('metadata', {}).get('writters', 'N/A')}\n"
        f"Episode Number: {episode.get('metadata', {}).get('ep_number', 'N/A')}\n"
        f"Scene: {scene if scene is not None else 'N/A'}\n"
        f"Content: {' '.join(actual_lines)}"
    )


def split_by_episode(text: str) -> list:
    episodes = []
    for i, raw_episode in enumerate(text.strip().split("End")):
        if not raw_episode.strip():
            continue

        episode_parts = re.split(pattern, raw_episode)
        first_part_lines = episode_parts[0].strip().split('\n')

        ep_name = first_part_lines[0].strip()
        writters = first_part_lines[1].strip() if len(first_part_lines) > 1 else None

        episodes.append({
            'metadata': {
                "ep_name": ep_name,
                "writters": writters.replace("Written by:", "").strip() if writters else None,
                "ep_number": i + 1
            },
            'content': raw_episode
        })

    return episodes


def generate_vector_base(episodes: list) -> list:
    lines = []
    for episode in episodes:
        episode_content = episode.get('content', '')

        # If the pattern exists, proceed to split and process
        for raw_line in re.split(pattern, episode_content):
            if not raw_line.strip():
                continue

            line_parts = raw_line.strip().split('\n')

            scene = line_parts[0].strip() if line_parts else None
            if scene and scene.startswith("[Scene:") and scene.endswith("]"):
                scene = scene.replace("[Scene:", "").replace("]", "").strip()
                actual_lines = line_parts[1:]

                lines.append({
                    **episode.get('metadata', {}),
                    "scene": scene,
                    "lines": actual_lines,
                    "raw_string": get_string_to_embed(episode, scene, actual_lines)
                })

    return lines
    

def chunk_content(path: pathlib.Path) -> list:
    with open(path, "r") as f:
        text = f.read()
    episodes = split_by_episode(text)
    lines = generate_vector_base(episodes)

    return lines