import type { AppPageDefinition } from '@/router/pageRegistryTypes'
import homePage from '@/standard/home/index'
import modelsPage from '@/standard/admin/models/index'
import previewPage from '@/standard/admin/preview/index'
import charactersPage from '@/standard/admin/characters/index'
import embedPage from '@/standard/admin/embed/index'

export const standardPageRegistry: AppPageDefinition[] = [
  homePage,
  modelsPage,
  previewPage,
  charactersPage,
  embedPage,
]
