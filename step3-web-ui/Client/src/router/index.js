import { createRouter, createWebHistory } from 'vue-router'
import ChatView from '../views/ChatView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: ChatView
  },
  {
    path: '/chat/:id',
    name: 'Chat',
    component: ChatView,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
