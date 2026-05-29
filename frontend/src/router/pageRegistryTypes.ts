import type { RouteRecordRaw } from 'vue-router'

export interface AppPageDefinition {
  routeName: string
  canonicalPath: string
  component: RouteRecordRaw['component']
  menuLabel?: string
  menuIcon?: string
}
