import Vue from "vue";
import Router from "vue-router";
import store from "./store";
import LoginPage from "./components/LoginPage.vue";
import SignupPage from "./components/SignupPage.vue";
import DashBoard from "./components/DashBoard.vue";
import FindPage from "./components/FindPage.vue";
import InfluencerRequests from "./components/InfluencerRequests.vue";
import ProfilePage from "./components/ProfilePage.vue";
import StatsPage from "./components/StatsPage.vue";
import InfluencerCampaigns from "./components/InfluencerCampaigns.vue";
import SponsorNotVerified from "./components/SponsorNotVerified.vue";
import FlaggedUser from "./components/FlaggedUser.vue";
import SponsorCampaigns from "./components/SponsorCampaigns.vue";
import SponsorCampaignView from "./components/SponsorCampaignView.vue";
import SponsorTransactions from "./components/SponsorTransactions.vue";
import AdminVerify from "./components/AdminVerify.vue";
import AdminFindCampaigns from "./components/AdminFindCampaigns.vue";
import AdminFlaggedCampaigns from "./components/AdminFlaggedCampaigns.vue";
import AdminFindUsers from "./components/AdminFindUsers.vue";
import AdminFlaggedUsers from "./components/AdminFlaggedUsers.vue";
import PaymentGateway from "./components/PaymentGateway.vue";

Vue.use(Router);

const router = new Router({
  mode : "hash",
  routes : [
    { path : "/login", component : LoginPage, meta : { title : "Login" } },
    { path : "/signup", component : SignupPage, meta : { title : "SignUp" } },
    { path : "/", component : DashBoard, meta : { title : "DashBoard", role : ["influencer", "sponsor", "admin"] } },
    { path : "/dashboard", component : DashBoard, meta : { title : "DashBoard", role : ["influencer", "sponsor", "admin"] } },
    { path : "/requests", component : InfluencerRequests, meta : { title : "Requests", role : ["influencer"] } },
    { path : "/find", component: FindPage, meta : { title : "Find", role : ["influencer", "sponsor"] } },
    { path : "/completed_campaigns", component : InfluencerCampaigns, meta : { title : "Completed Campaigns", role : ["influencer"] } },
    { path : "/profile", component : ProfilePage, meta : { title : "Profile", role : ["influencer", "sponsor"] } },
    { path : "/stats", component : StatsPage, meta : { title: "Stats", role : ["influencer", "sponsor"] } },
    { path : "/not_verified", component : SponsorNotVerified, meta : { title : "Not Verified", role : ["sponsor"] } },
    { path : "/flagged", component : FlaggedUser, meta : { title : "Flagged User", role : ["influencer", "sponsor"] } },
    { path : "/campaigns", component : SponsorCampaigns, meta : { title : "Campaigns", role : ["sponsor"] } },
    { path : "/campaigns/:id", component : SponsorCampaignView, meta : { title : "Campaign Details", role : ["sponsor"] }, props : true },
    { path : "/transactions", component: SponsorTransactions, meta : { title : "Transactions", role : ["sponsor"] } },
    { path : "/verify_sponsors", component: AdminVerify, meta : { title : "Verify Sponsors", role : ["admin"] } },
    { path : "/find_campaigns", component: AdminFindCampaigns, meta : { title : "Flag Campaigns", role : ["admin"] } },
    { path : "/flagged_campaigns", component: AdminFlaggedCampaigns, meta : { title : "Flagged Campaigns", role : ["admin"] } },
    { path : "/find_users", component: AdminFindUsers, meta : { title : "Flag Users", role : ["admin"] } },
    { path : "/flagged_users", component: AdminFlaggedUsers, meta : { title : "Flagged Users", role : ["admin"] } },
    { path : "/payment_gateway/:id", component: PaymentGateway, meta : { title : "Payment Gateway", role : ["sponsor"] }, props : true },
  ]
});

router.beforeEach(async (to, from, next) => {
  const role = store.state.auth.role || null;
  
  if (!role && (to.path == "/login" || to.path == "/signup")) {
    document.title = to.meta.title;
    return next();
  }

  if (!role) {
    store.commit("showAlert", { type: "warning", message: "Please Login!" });
    return next("/login");
  }
  
  if (!to.meta.role.includes(role)) {
    store.commit("showAlert", { type : "error", message : "You cannot access the page !" });
    return next(from.path);
  }

  try {
    let flaggedResponse = await Vue.prototype.$http.get("/auth/flagged", {
      headers: { Authorization: `Bearer ${store.state.auth.authToken}` },
    });

    let isFlagged = flaggedResponse.data;

    if (isFlagged && to.path !== "/flagged") {
      return next("/flagged");
    }

    if (!isFlagged && to.path === "/flagged") {
      return next("/");
    }

    if (role == "sponsor") {
      let verifiedResponse = await Vue.prototype.$http.get("/sponsor/verified", {
        headers : { Authorization: `Bearer ${store.state.auth.authToken}` },
      });

      let isVerified = verifiedResponse.data;

      if (!isVerified && to.path != "/not_verified") {
        return next("/not_verified");
      }

      if (isVerified && to.path == "/not_verified") {
        return next("/");
      }
    }

    document.title = to.meta.title + " | " + role[0].toUpperCase().concat(role.substring(1, ));
    next();
  } catch (error) {
    return next("/login");
  }
});


export default router;