<template>
  <div class="login-register">
    <div class="card">
      <div class="front q-pa-lg">
        <q-img src="https://sso-443.e1.buaa.edu.cn/cas/img/logo-full.png"
               height="225" width="45"
        />
        <div class="q-mb-lg">
          <div class="text-h6 q-mt-xl q-pa-sm text-weight-bold">计算机科学方法论</div>
          <div class="text-h5 text-primary q-pa-sm text-weight-bold">课程中心</div>
        </div>
        <div class="items-center q-mx-md">
          <q-form
            ref="form"
            v-model="valid"
            lazy-validation
          >

            <div>
              <q-input
                v-model="id"
                :rules="idRules"
                label="学号/工号"
                required
              >
                <template #label>
                  <div class="text-h5">
                    学号/工号
                  </div>
                </template>
              </q-input>

              <q-input
                v-model="name"
                label=""
                required
                maxlength="5"
              >
                <template #label>
                  <div class="text-h5">
                    姓名
                  </div>
                </template>
              </q-input>

              <q-input
                v-model="college"
                label=""
                required
              >
                <template #label>
                  <div class="text-h5">
                    学院
                  </div>
                </template>
              </q-input>

              <q-input
                v-model="password"
                :rules="[passwordRules]"
                :type="show2 ? 'text' : 'password'"
                label="密码"
                required
              >
                <template #append>
                  <q-avatar v-if="show2">
                    <q-btn
                      icon="visibility_off"
                      round
                      size="14px"
                      @click="show2 = !show2"
                    />
                  </q-avatar>
                  <q-avatar v-else>
                    <q-btn
                      icon="visibility"
                      round
                      size="14px"
                      @click="show2 = !show2"
                    />
                  </q-avatar>
                </template>
                <template #label>
                  <div class="text-h5">
                    密码
                  </div>
                </template>
              </q-input>

              <q-input
                v-model="rePassword"
                :type="show3 ? 'text' : 'password'"
                :rules="[passwordRules, affirmPass]"
                lazy-rules
                label="确认密码"
                type="password"
                required
              >
                <template #append>
                  <q-avatar v-if="show3">
                    <q-btn
                      icon="visibility_off"
                      round
                      size="14px"
                      @click="show3 = !show3"
                    />
                  </q-avatar>
                  <q-avatar v-else>
                    <q-btn
                      icon="visibility"
                      round
                      size="14px"
                      @click="show3 = !show3"
                    />
                  </q-avatar>
                </template>
                <template #label>
                  <div class="text-h5">
                    确认密码
                  </div>
                </template>
              </q-input>


              <q-input
                v-model="Email"
                label="邮箱"
                type="email"
                lazy-rules
                suffix="@buaa.edu.cn"
                required
              >
                <template #label>
                  <div class="text-h5">
                    邮箱
                  </div>
                </template>
              </q-input>

              <div class="text-center">
              <q-btn
                :disabled="!valid"
                class="button"
                large
                @click="Register"
              >
                <p class="login_">
                  注册
                </p>
              </q-btn>
              </div>
            </div>
          </q-form>
        </div>
        <div>
          <div class="row">
            <div class="col-12 text-center">
              <q-btn
                flat
                color="primary"
                class="return"
                to="/login"
              >
                登录
              </q-btn>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  "data": () => ({
    "show2": false,
    "show3": false,
    "valid": true,
    "id": "",
    "idRules": [(v) => !!v || "ID is required"],
    "name": "",
    "college": "",
    "password": "",
    "passwordRules": (v) => !!v || "请填写密码",
    "rePassword": "",
    "Email": "",
    "emailRules": [
      v => !!v || "E-mail is required",
      v => /.+@.+\..+/.test(v) || "E-mail must be valid",
    ],
    "checkbox": false,
    "role" : "学生",
    "options" : ["管理员", "教师", "学生"]
  }),

  "methods": {
    postCreate() {
      // console.log(this.role, this.options, this.options.indexOf(this.role))
      this.$api({
        "method": "POST",
        "url": "api/user",
        "data": {
          identity: this.options.indexOf(this.role),
          id: this.id,
          name: this.name,
          college: this.college,
          pwd: this.password,
          mail: this.Email
        },
      }).then(res => {
        console.log("注册", res);
        if (res.status === 200) {

          alert("注册成功，正在前往登录界面");
          this.$router.push({ "path": "/login" });

        } else if (res.status === 0) {
          alert(res.message)
          // this.clear()
        }

      });
    },
    Register () {
      this.$refs.form.validate()
        .then(success => {
          if (success) {
            this.postCreate()
          }
        })

    },
    clear () {

      this.id = "";
      this.password = "";
      this.rePassword = "";
      this.Email = "";

    },
    affirmPass (val) {

      if (val !== this.password) {

        return "两次密码不一致";

      }
      return true;

    },
  },
};
</script>

