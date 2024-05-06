def "nu-complete b5 task-names" [] {
  ^b5 --quiet help --tasks | lines | str trim
}

# b5 task runner
export extern b5 [
  --help(-h)
  --quiet(-q)
  --config(-c): string
  --taskfile(-t): string
  --project-path(-p): string
  --run-path(-r): string
  --detect(-d): string
  --shell(-s): string
  task_name?: string@"nu-complete b5 task-names"
  ...args
]
