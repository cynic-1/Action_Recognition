const routes = [
  {
    "path": "/",
    "component": () => import("layouts/MainLayout.vue"),
    "children": [
      { "path": "", redirect: '/home/:id' },
      { "path": "analysis/:id", "component": () => import("pages/Analysis") },
      { "path": "class", "component": () => import("pages/Class") },
      { "path": "course", "component": () => import("pages/Course") },
      { "path": "student", "component": () => import("pages/Student") },
      { "path": "videos", "component": () => import("pages/StuVideoList") },
      { "path": "rate", "component": () => import("pages/Rate") },
      { "path": "home/:id", "component": () => import("pages/Home") },
    ]
  },
  {
    "path": "/login",
    "component": () => import("pages/Login")
  },
  {
    "path": "/register",
    "component": () => import("pages/Register")
  },
  {
    "path": "/3d",
    "component": () => import("pages/WebGL")
  },
  {
    "path": "/2d",
    "component": () => import("pages/2D")
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    "path": "/:catchAll(.*)*",
    "component": () => import("pages/Error404.vue")
  }
];

export default routes;
