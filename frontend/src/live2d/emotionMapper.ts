import type { Live2DActions } from '@/live2d/types'

export function applyExpressions(
  actions: Live2DActions | null | undefined,
  onExpression?: (expr: number | string) => void,
): void {
  if (!actions?.expressions?.length) return
  for (const expr of actions.expressions) {
    onExpression?.(expr)
  }
}

export function expressionLabel(
  expr: number | string,
  emotionMap: Record<string, unknown>,
): string {
  for (const [key, value] of Object.entries(emotionMap)) {
    if (value === expr) return key
  }
  return String(expr)
}
