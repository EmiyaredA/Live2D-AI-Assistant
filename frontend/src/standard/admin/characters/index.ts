import type { AppPageDefinition } from '@/router/pageRegistryTypes'

const page: AppPageDefinition = {
  routeName: 'AdminCharacters',
  canonicalPath: '/admin/characters',
  menuLabel: '角色画像',
  component: () => import('./page.vue'),
}

export default page
