import {
  RadarChart as RechartsRadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  Legend,
  ResponsiveContainer,
  Tooltip,
} from 'recharts'

const AXES = [
  { key: 'study_hours',         label: 'Study Hours',   max: 12 },
  { key: 'sleep_hours',         label: 'Sleep',         max: 12 },
  { key: 'mental_health_score', label: 'Mental Health', max: 10 },
  { key: 'focus_index',         label: 'Focus',         max: 100 },
  { key: 'productivity_score',  label: 'Productivity',  max: 100 },
  { key: 'exercise_minutes',    label: 'Exercise',      max: 120 },
  { key: 'social_media_hours',  label: 'Social Media',  max: 12,  invert: true },
  { key: 'burnout_level',       label: 'Burnout',       max: 100, invert: true },
]

// Dataset averages (approximate from StudentDataset.csv)
const DATASET_AVERAGES = {
  study_hours: 5.1,
  sleep_hours: 7.3,
  mental_health_score: 7.1,
  focus_index: 62.0,
  productivity_score: 61.0,
  exercise_minutes: 45.0,
  social_media_hours: 3.2,
  burnout_level: 42.0,
}

function normalize(value, max, invert = false) {
  const norm = Math.min(100, (value / max) * 100)
  return invert ? 100 - norm : norm
}

export default function RadarChart({ studentInput, animationDuration = 1200 }) {
  const data = AXES.map(({ key, label, max, invert }) => ({
    subject: label,
    student: normalize(studentInput?.[key] ?? 0, max, invert),
    average: normalize(DATASET_AVERAGES[key] ?? 0, max, invert),
  }))

  return (
    <ResponsiveContainer width="100%" height={320}>
      <RechartsRadarChart data={data} margin={{ top: 10, right: 30, bottom: 10, left: 30 }}>
        <PolarGrid stroke="#1E1E2E" />
        <PolarAngleAxis
          dataKey="subject"
          tick={{ fill: '#8B8AA0', fontSize: 11, fontFamily: 'Satoshi, sans-serif' }}
        />
        <Radar
          name="You"
          dataKey="student"
          stroke="#6C63FF"
          fill="#6C63FF"
          fillOpacity={0.2}
          animationDuration={animationDuration}
        />
        <Radar
          name="Average"
          dataKey="average"
          stroke="#00D4AA"
          fill="#00D4AA"
          fillOpacity={0.1}
          strokeDasharray="4 4"
          animationDuration={animationDuration}
        />
        <Legend
          wrapperStyle={{ color: '#8B8AA0', fontSize: 12, fontFamily: 'Satoshi, sans-serif' }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: '#16161F',
            border: '1px solid #1E1E2E',
            borderRadius: '12px',
            color: '#F0EEF8',
            fontSize: 12,
          }}
          formatter={(value, name) => [`${value.toFixed(0)}%`, name]}
        />
      </RechartsRadarChart>
    </ResponsiveContainer>
  )
}
