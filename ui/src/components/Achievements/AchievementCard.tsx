import achievements from './achievements.data';

export default function AchievementCard({ figure, suffix, color, barColor, bar, description, active }: typeof achievements[0] & { active: boolean }) {
  return (
    <div className="flex flex-col gap-3 bg-white rounded-2xl px-6 py-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-300">
      <div
        className={`text-5xl font-black tracking-tight ${color} transition-opacity duration-700 delay-300 ${active ? 'opacity-100' : 'opacity-0'}`}
      >
        {figure}{suffix ?? ''}
      </div>
      <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${barColor} transition-all duration-1000 ease-out`}
          style={{ width: active ? `${bar}%` : '0%' }}
        />
      </div>
      <p className="text-sm text-gray-600 leading-relaxed">{description}</p>
    </div>
  )
}
