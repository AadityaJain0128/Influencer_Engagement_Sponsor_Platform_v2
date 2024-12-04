import Vue from 'vue';
import Vuex from 'vuex';


Vue.use(Vuex);

export default new Vuex.Store({
  state : {
    alert : {
      type : "",
      message : ""
    },

    auth : {
      role : localStorage.getItem("role") || "",
      authToken : localStorage.getItem("authToken") || "",
      username : localStorage.getItem("username") || "",
      email : localStorage.getItem("email") || "",
      profile : localStorage.getItem("profile") || ""
    },
    
    info : {
      id : localStorage.getItem("id") || "",
      name : localStorage.getItem("name") || "",
      category : localStorage.getItem("category") || "",
      reach : localStorage.getItem("reach") || "",
      socials : JSON.parse(localStorage.getItem("socials")) || {}
    }
  },

  getters : {
    authToken(state) {
      return state.auth.authToken;
    }
  },

  mutations : {
    showAlert(state, { type, message }) {
      state.alert = { type, message };
    },
    dismissAlert(state) {
      state.alert.message = "";
    },

    setAuth(state, { role, authToken, username, email }) {
      localStorage.setItem("role", role);
      localStorage.setItem("authToken", authToken);
      localStorage.setItem("username", username);
      localStorage.setItem("email", email);
      state.auth = { role, authToken, username, email };
    },
    setProfileImage(state, url) {
      localStorage.setItem("profile", url);
      state.auth.profile = url;
    },
    logOut(state) {
      state.auth = { role : "", authToken : "", username : "", email : "" };
      state.info = { id : "", name : "", category : "", reach : "", socials : "" };

      localStorage.clear();
    },

    setInfo(state, { id, name, category, reach, socials }) {
      localStorage.setItem("id", id);
      localStorage.setItem("name", name);
      localStorage.setItem("category", category);
      localStorage.setItem("reach", reach);
      localStorage.setItem("socials", JSON.stringify(socials))
      state.info = { id, name, category, reach, socials };
    },
  },

  actions : {
    async fetchProfileImage({ state, commit }, context) {
      let response = await context.$http.get("/auth/profile-image", {
        headers : { "Authorization" : `Bearer ${state.auth.authToken}` }
      });
      commit("setProfileImage", response.data.url);
    }
  }
});
