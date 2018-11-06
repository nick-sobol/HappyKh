import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import ConfirmRegistration from './views/ConfirmRegistration.vue';
import CreatePlace from './views/CreatePlace.vue';
import PlaceDetail from './views/Place.vue';
import Profile from './views/Profile.vue';
import ProfileSettings from './views/ProfileSettings.vue';
import store from './store';
import axiosInstance from './axios-config';

const ifAuthenticated = (to, from, next) => {
  if (store.getters.getAuthenticated) {
    next();
  } else {
    next({ name: 'login' });
  }
};

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/confirm_registration/:userId/:emailToken',
      name: 'confirm_registration',
      component: ConfirmRegistration,
    },
    {
      path: '/profile/settings',
      name: 'settings',
      component: ProfileSettings,
      beforeEnter: ifAuthenticated,
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: Profile,
      beforeEnter: ifAuthenticated,
    },
    {
      path: '/places/create',
      name: 'createPlace',
      component: CreatePlace,
      beforeEnter: ifAuthenticated,
    },
    {
      path: '/places/:id',
      name: 'placeDetail',
      component: PlaceDetail,
      beforeEnter: ifAuthenticated,
    },
  ],
});

router.beforeEach((to, from, next) => {
  if (store.getters.getAuthenticated) {
    axiosInstance.get('api/users/token-validation')
      .then((response) => {
        next();
      }).catch((error) => {
        store.dispatch('signOut');
        next({ name: 'login' });
      });
  } else {
    next();
  }
});

Vue.use(Router);

export default router;
