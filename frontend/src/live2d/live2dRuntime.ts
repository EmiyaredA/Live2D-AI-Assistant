import * as PIXI from 'pixi.js'
import { Live2DModel } from 'pixi-live2d-display/cubism4'

let initialized = false

export function ensureLive2DRuntime(): void {
  if (initialized) return
  if (typeof window.Live2DCubismCore === 'undefined') {
    throw new Error('Live2DCubismCore 未加载，请在 index.html 引入 live2dcubismcore.min.js')
  }
  ;(window as unknown as { PIXI: typeof PIXI }).PIXI = PIXI
  Live2DModel.registerTicker(PIXI.Ticker)
  initialized = true
}

export type PixiLive2DModel = InstanceType<typeof Live2DModel>

export async function loadLive2DModel(modelUrl: string): Promise<PixiLive2DModel> {
  ensureLive2DRuntime()
  return Live2DModel.from(modelUrl, { autoInteract: false })
}

export function setModelParameter(model: PixiLive2DModel, paramId: string, value: number): void {
  const core = (model.internalModel as { coreModel?: { setParameterValueById: (id: string, v: number) => void } })
    .coreModel
  core?.setParameterValueById(paramId, value)
}

export async function applyModelExpression(
  model: PixiLive2DModel,
  expression: number | string,
): Promise<void> {
  try {
    await model.expression(expression)
  } catch {
    // shizuku 等无 Expression 的模型忽略
  }
}

declare global {
  interface Window {
    Live2DCubismCore?: unknown
    PIXI?: typeof PIXI
  }
}
