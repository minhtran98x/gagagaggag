import { createRouter, createWebHistory } from "vue-router";
import { userResource } from "@/stores/user";
import { sessionStore } from "@/stores/session";

const routes = [
  {
    path: "/",
    redirect: { name: "ats_institutions" },
    name: "Home",
  },
  {
    path: '/yyys',
    name: 'yyys',
    component: () => import('@/pages/yyy/yyys.vue'),
  },
  {
    path: '/yyys/:yyyId',
    name: 'yyy',
    component: () => import(`@/pages/yyy/yyy.vue`),
    props: true,
  },
  {
    path: '/yyyNew',
    name: 'yyyNew',
    component: () => import(`@/pages/yyy/yyyNew.vue`),
  },
  {
    path: '/ats_institutions',
    name: 'ats_institutions',
    component: () => import('@/pages/ats_institution/list.vue'),
  },
  {
    path: '/ats_institutions/:yyyId',
    name: 'ats_institution',
    component: () => import(`@/pages/ats_institution/detail.vue`),
    props: true,
  },
  {
    path: '/atsInstitutionNew',
    name: 'atsInstitutionNew',
    component: () => import(`@/pages/ats_institution/new.vue`),
  },
  {
    path: '/ats_companies',
    name: 'ats_companies',
    component: () => import('@/pages/ats_company/list.vue'),
  },
  {
    path: '/ats_companies/:yyyId',
    name: 'ats_company',
    component: () => import(`@/pages/ats_company/detail.vue`),
    props: true,
  },
  // {
  //   path: '/atsInstitutionNew',
  //   name: 'atsInstitutionNew',
  //   component: () => import(`@/pages/ats_institution/new.vue`),
  // }
];

const handleMobileView = (componentName) => {
  return window.innerWidth < 768 ? `Mobile${componentName}` : componentName;
};

const scrollBehavior = (to, from, savedPosition) => {
  if (to.name === from.name) {
    to.meta?.scrollPos && (to.meta.scrollPos.top = 0);
    return { left: 0, top: 0 };
  }
  const scrollpos = to.meta?.scrollPos || { left: 0, top: 0 };

  if (scrollpos.top > 0) {
    setTimeout(() => {
      let el = document.querySelector("#list-rows");
      el.scrollTo({
        top: scrollpos.top,
        left: scrollpos.left,
        behavior: "smooth",
      });
    }, 300);
  }
};

let router = createRouter({
  history: createWebHistory("/xxx"),
  routes,
  scrollBehavior,
});

router.beforeEach(async (to, from, next) => {
  const { isLoggedIn } = sessionStore();

  isLoggedIn && (await userResource.promise);

  // if (from.meta?.scrollPos) {
  //   from.meta.scrollPos.top = document.querySelector("#list-rows")?.scrollTop;
  // }

  if (to.name === "Home" && isLoggedIn) {
    next({ name: "ats_institutions" });
  } else if (!isLoggedIn) {
    window.location.href = "/login?redirect-to=/xxx";
  } else {
    next();
  }
});

export default router;
