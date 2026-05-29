import type { AppPageDefinition } from '@/router/pageRegistryTypes'

const page: AppPageDefinition = {
  routeName: 'AdminEmbed',
  canonicalPath: '/admin/embed',
  menuLabel: '嵌入管理',
  component: () => import('./page.vue'),
}

export default page
