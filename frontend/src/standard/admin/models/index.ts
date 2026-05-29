import type { AppPageDefinition } from '@/router/pageRegistryTypes'

const page: AppPageDefinition = {
  routeName: 'AdminModels',
  canonicalPath: '/admin/models',
  menuLabel: '模型管理',
  component: () => import('./page.vue'),
}

export default page
