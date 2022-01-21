module.exports = {
  // https://eslint.org/docs/user-guide/configuring#configuration-cascading-and-hierarchy
  // This option interrupts the configuration hierarchy at this file
  // Remove this if you have an higher level ESLint config file (it usually happens into a monorepos)
  root: true,

  parserOptions: {
    parser: '@babel/eslint-parser',
    ecmaVersion: 2018, // Allows for the parsing of modern ECMAScript features
    sourceType: 'module' // Allows for the use of imports
  },

  env: {
    browser: true
  },

  // Rules order is important, please avoid shuffling them
  extends: [
    // Base ESLint recommended rules
    // 'eslint:recommended',


    // Uncomment any of the lines below to choose desired strictness,
    // but leave only one uncommented!
    // See https://eslint.vuejs.org/rules/#available-rules
    'plugin:vue/vue3-essential', // Priority A: Essential (Error Prevention)
    // 'plugin:vue/vue3-strongly-recommended', // Priority B: Strongly Recommended (Improving Readability)
    // 'plugin:vue/vue3-recommended', // Priority C: Recommended (Minimizing Arbitrary Choices and Cognitive Overhead)

    // https://github.com/prettier/eslint-config-prettier#installation
    // usage with Prettier, provided by 'eslint-config-prettier'.
    'prettier'
  ],

  plugins: [
    // https://eslint.vuejs.org/user-guide/#why-doesn-t-it-work-on-vue-file
    // required to lint *.vue files
    'vue',

    // https://github.com/typescript-eslint/typescript-eslint/issues/389#issuecomment-509292674
    // Prettier has not been included as plugin to avoid performance impact
    // add it as an extension for your IDE
  ],

  globals: {
    ga: 'readonly', // Google Analytics
    cordova: 'readonly',
    __statics: 'readonly',
    __QUASAR_SSR__: 'readonly',
    __QUASAR_SSR_SERVER__: 'readonly',
    __QUASAR_SSR_CLIENT__: 'readonly',
    __QUASAR_SSR_PWA__: 'readonly',
    process: 'readonly',
    Capacitor: 'readonly',
    chrome: 'readonly'
  },

  // add your custom rules here
  rules: {
    'prefer-promise-reject-errors': 'off',
    "no-console": 0,
    "prefer-const": "warn",
    "no-var": "error",
    "no-new-object": "warn",
    "object-shorthand": "warn",
    "quote-props": "warn",
    "no-array-constructor": "warn",
    "array-callback-return": "warn",
    "prefer-destructuring": "warn",
    "prefer-template": "warn",
    "template-curly-spacing": "warn",
    "no-eval": "error",
    "func-style": "warn",
    "no-loop-func": "warn",
    "prefer-rest-params": "warn",
    "no-new-func": "warn",
    "no-param-reassign": "error",
    "prefer-spread": "warn",
    "function-paren-newline": "warn",
    "prefer-arrow-callback": "warn",
    "arrow-spacing": "warn",
    "implicit-arrow-linebreak": ["warn", "beside"],
    "no-duplicate-imports": "error",
    "sort-imports": "warn",
    "no-iterator": "warn",
    "dot-notation": "warn",
    "no-undef-init": "error",
    "one-var": ["warn","never"],
    "no-multi-assign": "warn",
    "no-plusplus": "error",
    "eqeqeq": "error",
    "no-case-declarations": "warn",
    "no-nested-ternary": "warn",
    "no-unneeded-ternary": "warn",
    "brace-style": "warn",
    "no-else-return": "warn",
    "spaced-comment": "warn",
    "keyword-spacing": "warn",
    "space-infix-ops": "warn",
    "padded-blocks": "warn",
    "space-in-parens": "warn",
    "array-bracket-spacing": ["warn", "never"],
    "object-curly-spacing": ["warn", "always"],
    "comma-spacing": ["warn", { "before": false, "after": true }],
    "key-spacing": ["warn", { "beforeColon": false }],
    "comma-style": ["warn", "last"],
    "semi": ["warn", "always"],
    "camelcase": "warn",
    "new-cap": "warn",
    "no-underscore-dangle": "warn",

    // allow debugger during development only
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off'
  }
}
