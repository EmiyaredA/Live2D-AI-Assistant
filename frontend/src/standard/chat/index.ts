import type { AppPageDefinition } from '@/router/pageRegistryTypes'

const page: AppPageDefinition = {
  routeName: 'Chat',
  canonicalPath: '/chat',
  menuLabel: '对话',
  component: () => import('./page.vue'),
}

export default page
