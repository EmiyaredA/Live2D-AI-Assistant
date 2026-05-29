import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import MainLayout from '@/layout/MainLayout.vue'
import { standardPageRegistry } from '@/router/pageRegistry'

const children: RouteRecordRaw[] = [
  ...standardPageRegistry.map((page) => ({
    path: page.canonicalPath === '/' ? '' : page.canonicalPath.replace(/^\//, ''),
    name: page.routeName,
    component: page.component!,
    meta: { menuLabel: page.menuLabel, menuIcon: page.menuIcon },
  })),
  {
    path: 'admin/preview/:modelId',
    name: 'AdminPreviewModel',
    component: () => import('@/standard/admin/preview/page.vue'),
    meta: { menuLabel: '模型预览' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: MainLayout,
      children,
    },
    {
      path: '/chat/:characterId',
      name: 'ChatStandalone',
      component: () => import('@/standard/chat/page.vue'),
      meta: { standalone: true },
    },
  ],
})

export default router
