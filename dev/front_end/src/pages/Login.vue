<template>
  <div class="login-register">
    <div class="card">
      <div
        id="1"
        class="front q-pa-lg"
        :class="{'contain-Before': isTop}"
      >
          <q-img src="https://sso-443.e1.buaa.edu.cn/cas/img/logo-full.png"
          height="225" width="45"
          />
        <div class="q-mb-lg">
          <div class="text-h6 q-mt-xl q-pa-sm text-weight-bold">计算机科学方法论</div>
          <div class="text-h5 text-primary q-pa-sm text-weight-bold">课程中心</div>
          <br><br>
        </div>
        <div class="items-center q-mx-md">
          <q-form
            ref="form"
            lazy-validation
          >
            <div>
              <div class="row items-center">
                <div class="col-12">
                  <q-input
                    v-model="id"
                    :rules="idRules"
                    label=""
                    required
                  >
                    <template #label>
                      <div class="text-h5">
                        学工号
                      </div>
                    </template>
                  </q-input>

                  <q-input
                    v-model="password"
                    :rules="passwordRules"
                    :type="show1 ? 'text' : 'password'"
                    label=""
                    required
                  >
                    <template #append>
                      <q-avatar v-if="show1">
                        <q-btn
                          icon="visibility_off"
                          round
                          size="14px"
                          @click="show1 = !show1"
                        />
                      </q-avatar>
                      <q-avatar v-else>
                        <q-btn
                          icon="visibility"
                          round
                          size="14px"
                          @click="show1 = !show1"
                        />
                      </q-avatar>
                    </template>
                    <template #label>
                      <div class="text-h5">
                        密码
                      </div>
                    </template>
                  </q-input>
                  <!--                  :disabled="!valid"-->
                  <div class="text-center">
                  <q-btn
                    class="button"
                    large
                    @click="Login"
                  >
                    <p class="login_">
                      登 录
                    </p>
                  </q-btn>
                  </div>
                </div>
              </div>
            </div>
          </q-form>
        </div>
        <div>
          <div class="col-12 items-center text-center">
            <q-btn
              flat
              color="primary"
              class="register"
              to="/register"
            >
              注册
            </q-btn>
            <q-btn
              flat
              color="primary"
              class="forget"
              to="/forgetPassword"
            >
              忘记密码
            </q-btn>
          </div>
        </div>
      </div>
    </div>
    <q-dialog v-model="toolbar">
      <q-card style="height: 150px;width: 350px">
        <q-toolbar>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo.svg" alt="logo">
          </q-avatar>

          <q-toolbar-title><span class="text-weight-bold" style="font-size: 25px">登录</span><span
            style="font-size: 25px">信息</span></q-toolbar-title>

          <q-btn flat round dense icon="close" v-close-popup/>
        </q-toolbar>

        <q-card-section>
          <span style="font-size: 20px">登录成功，即将为您进行页面跳转</span>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="toolbar1">
      <q-card style="height: 150px;width: 350px">
        <q-toolbar>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo.svg" alt="logo">
          </q-avatar>

          <q-toolbar-title><span class="text-weight-bold" style="font-size: 25px">管理员</span><span
            style="font-size: 25px">登录信息</span></q-toolbar-title>

          <q-btn flat round dense icon="close" v-close-popup/>
        </q-toolbar>

        <q-card-section>
          <span style="font-size: 20px">身份验证管理员登录成功，即将为您进行页面跳转</span>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      toolbar: false,
      toolbar1: false,
      "valid": true,
      "show1": false,
      "show2": false,
      "show3": false,
      "isTop": false,
      "id": "",
      "idRules": [(v) => !!v || "请填写用户名/邮箱"],
      "password": "",
      "passwordRules": [(v) => !!v || "请填写密码"],
      "message": "error",
    };
  },
  "methods": {
    Login() {
      this.validate();
      // if(this.role === "教师")
      //   this.$router.push("/class")
      // else if(this.role === "学生")
      //   this.$router.push("/upload")
      // else
      //   alert("尚未开放")
      console.log(this.id, this.password)
      this.$api({
        "method": "POST",
        "url": "api/user/login",
        "header": {'Content-Type': 'application/json'},
        "data": {
          id: this.id,
          pwd: this.password
        },
      }).then(res => {
        console.log("登录", res);
        if (res.status === 200) {
          alert("登录成功");
          this.toolbar = true
          console.log(res.data)
          clearTimeout(this.timer);  //清除延迟执行
          sessionStorage.setItem('userId', res.data._id)
          console.log(sessionStorage.getItem('userId'))
          this.$router.push({"path": "/home/"+res.data._id})
          // this.timer = setTimeout(()=>{   //设置延迟执行
          //   this.$router.push({"path": "/", "query": {"user_id": localStorage.getItem('userId')}});
          // },2000);
        } else if (res.status === 800) {
          alert(res.message)
        } else if (res.status === 0) {
          this.toolbar1 = true;
          clearTimeout(this.timer);  //清除延迟执行
          this.timer = setTimeout(()=>{   //设置延迟执行
            this.$router.push({"path": "/administrator"});
          },2000);
        }
      });

    },
    validate() {
      this.$refs.form.validate();
    },
    clear() {
      this.id = "";
      this.password = "";
    },
    affirmPass(val) {
      if (val !== this.password) {
        return "两次密码不一致";
      }
      return true;
    },
  },
};
</script>

<style>
.login-register {
  background-image: url('../assets/bg1.jpg');
  width: 100%;
  height: 100vh;
}

.button {
  color: white;
  /*box-shadow: 9px 9px 18px rgba(0, 0, 0, 0.1),*/
  /*-9px -9px 18px rgba(255, 255, 255, 1);*/
  /*transition: box-shadow 0.2s ease-out;*/
  background-color: var(--q-primary);
  position: relative;
  top: 15%;
  margin-top: 20px;
  width: 100%;
  height: 40px;
  outline: none;
  border: none;
}

.login_ {
  font-size: 18px;
  font-family: "Microsoft YaHei UI";
}

.card {
  position: absolute;
  right: 0;
  top: 0;
  /*transform: translate(-50%, -50%);*/
  height: 100%;
  width: 320px;
  transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.card .front,
.card .back {
  position: absolute;
  /*box-shadow: 12px 12px 24px rgba(0, 0, 0, 0.1),*/
  /*-12px -12px 24px rgba(255, 255, 255, 1);*/
  /*border-radius: 3rem;*/
  background-color: #efeeee;
  opacity: 0.8;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: 1s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.front,
.back {
  position: absolute;
  transition: 0.3s linear;
  backface-visibility: hidden;
}

.register {
  top: 130px;
}

.forget {
  top: 130px;
}

.turn {
  text-align: right;
}

.back {
  transform: rotateY(-180deg);
}

.front {
  transform: rotateY(0deg);
}

.return {
  top: 40px;
}

.card .contain-Before {
  transform: rotateY(-180deg);
}

.card .contain-After {
  transform: rotateY(0deg);
}
</style>
