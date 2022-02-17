const routes = [
  {
    "path": "/",
    "component": () => import("layouts/MainLayout.vue"),
    "children": [
      // { "path": "", "component": () => import("pages/Index.vue") },
      { "path": "analysis", "component": () => import("pages/Analysis") },
      { "path": "class", "component": () => import("pages/Class") },
      { "path": "course", "component": () => import("pages/Course") },
      { "path": "student", "component": () => import("pages/Student") },
      { "path": "stuvideolist", "component": () => import("pages/StuVideoList") },
      { "path": "rate", "component": () => import("pages/Rate") },
      { "path": "home/:id", "component": () => import("pages/PersonalUpload") },
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
  // Always leave this as last one,
  // but you can also remove it
  {
    "path": "/:catchAll(.*)*",
    "component": () => import("pages/Error404.vue")
  }
];

export default routes;
