import VueRouter from 'vue-router'
 
import ChatHome from '../view/pages/chatHome/index.vue'
import Video from '../view/pages/video.vue'
import Lingting from '../view/pages/lingting.vue'
import Setting from '../view/pages/setting.vue'
import ChatWindow from '../view/pages/chatHome/chatwindow.vue'
import Experience from '../view/pages/experience.vue'
import Company from '../view/pages/company.vue'
 
export default new VueRouter({
    routes: [
        {
            path: "/",
            redirect: "/ChatHome",
          },
        {
            path: "/ChatHome",
            name: "ChatHome",
            component: ChatHome,
        },    
        {
            path: "/Video",
            name: "Video",
            component: Video
        }, 
        {
            path: "/Lingting",
            name: "Lingting",
            component: Lingting
        },   
        {
            path: "/Setting",
            name: "Setting",
            component: Setting
        },    
        {
            path: "/Experience",
            name: "Experience",
            component: Experience
        }, 
        {
            path: "/Company",
            name: "Company",
            component: Company
        },
    ]
})