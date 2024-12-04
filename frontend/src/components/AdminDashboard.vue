<template>
    <div id="container">
        <h1 align="center">Welcome {{ name }}</h1>
        <div id="stats" class="mt-5">
            <div class="d-flex justify-content-center">
                <Bar :data="userData" :options="userOptions" id="users" style="width:100%; max-width:950px; max-height: 500px"></Bar>
            </div>
            <br><br>
            <div style="width: 47%; float: left;">
                <Pie :data="campaignData" :options="campaignData" id="campaigns" style="width:100%; max-width:700px; max-height: 300px;"></Pie>
                <br>
                <div align="center"><span>Total Campaigns<br>{{ total_campaigns }}</span></div>
                <br><br>
                <Doughnut :data="flaggedData" :options="flaggedOptions" id="flagged_campaigns" style="width:100%; max-width:700px; max-height: 300px;"></Doughnut>
                <br><br>
                <Bar :data="sponsorData" :options="sponsorOptions" id="sponsor_industry" style="width:100%; max-width:700px; max-height: 300px;"></Bar>
            </div>
            <div style="width: 47%; float: right;">
                <Bar :data="transactionData" :options="transactionOptions" id="transactions" style="width:100%; max-width:700px; max-height: 300px;"></Bar>
                <br>
                <div align="center">
                    <span>
                        Average Pay Amount
                        <br>
                        {{ avg_amount }}
                    </span>
                </div>
                <br><br>
                <Doughnut :data="statusData" :options="statusOptions" id="campaign_status" style="width:100%; max-width:700px; max-height: 300px;"></Doughnut>
                <br><br>
                <Bar :data="influencerData" :options="influencerOptions" id="influencer_niche" style="width:100%; max-width:700px; max-height: 300px;"></Bar>
            </div>
        </div>
    </div>
</template>


<script>
    import { Pie, Bar, Doughnut } from 'vue-chartjs';
    import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js';

    ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);

    export default {
        name : "AdminDashboard",
        components : {
            Pie, Bar, Doughnut
        },
        data() {
            return {
                user_labels : [],
                user_values : [],
                campaign_labels : [],
                campaign_values : [],
                transaction_labels : [],
                transaction_values : [],
                flagged_labels : [],
                flagged_values : [],
                category_labels : [],
                i_values : [],
                s_values : [],
                request_labels : [],
                request_values : [],
                status_labels : [],
                status_values : []
            }
        },
        methods : {
            async getDetails() {
                let { data } = await this.$http.get("/admin/getDetails", {
                    headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` }
                });

                if (data.status == "success") {
                    this.$store.commit("setInfo", { id : data.id, name : data.name, category : "", reach : "", socials : {} });
                }
            },
            async getData() {
                let { data } = await this.$http.get("/admin/getData", {
                    headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` }
                });

                if (data.status == "success") {
                    this.user_labels = data.user_labels;
                    this.user_values = data.user_values;
                    this.campaign_labels = data.campaign_labels;
                    this.campaign_values = data.campaign_values;
                    this.transaction_labels = data.transaction_labels;
                    this.transaction_values = data.transaction_values;
                    this.flagged_labels = data.flagged_labels,
                    this.flagged_values = data.flagged_values,
                    this.category_labels = data.category_labels,
                    this.i_values = data.i_values,
                    this.s_values = data.s_values,
                    this.request_labels = data.request_labels,
                    this.request_values = data.request_values,
                    this.status_labels = data.status_labels,
                    this.status_values = data.status_values
                }
            },
            
            randomizeColor() {
                const hex = "0123456789ABCDEF";
                let color_code = "#";
                for (let i = 0; i < 6; i++) {
                    color_code += hex[parseInt(Math.random() * 16)]
                }
                return color_code
            }
        },
        computed : {
            name() {
                return this.$store.state.info.name;
            },
            total_campaigns() {
                return this.campaign_values.reduce((a, b) => a + b, 0);
            },
            avg_amount() {
                return this.transaction_values.length == 0 ? 0 : (this.transaction_values.reduce((a, b) => a + b, 0) / this.transaction_values.length).toFixed(2)
            },
            userData() {
                return {
                    labels : this.user_labels,
                    datasets : [{
                        data : this.user_values,
                        backgroundColor: this.user_values.map(() => this.randomizeColor())
                    }]
                }
            },
            userOptions() {
                return {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Role Distribution',
                        },
                        legend: {
                            display: false,
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'No. of Users'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Roles'
                            }
                        }
                    }
                }
            },
            campaignData() {
                return {
                    labels: this.campaign_labels,
                    datasets: [{
                        data: this.campaign_values,
                        backgroundColor: ["green", "orange", "blue"]
                    }]
                };
            },
            campaignOptions() {
                return {
                    responsive: true
                };
            },
            transactionData() {
                return {
                    labels: this.transaction_labels,
                    datasets: [{
                        data: this.transaction_values,
                        backgroundColor: this.transaction_values.map(() => this.randomizeColor())
                    }]
                };
            },
            transactionOptions() {
                return {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Transactions',
                        },
                        legend: {
                            display: false,
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Budget'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Completed Campaigns'
                            }
                        }
                    }
                };
            },
            flaggedData() {
                return {
                    labels: this.flagged_labels,
                    datasets: [{
                        data: this.flagged_values,
                        backgroundColor: ["red", "green"]
                    }]
                }
            },
            flaggedOptions() {
                return {
                    title: {
                        display: true,
                        text: "Flagged Campaigns"
                    }
                }
            },
            statusData() {
                return {
                    labels: this.status_labels,
                    datasets: [{
                        data: this.status_values,
                        backgroundColor: this.status_values.map(() => this.randomizeColor())
                    }]
                }
            },
            statusOptions() {
                return {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: "Campaign Visibility"
                        }
                    }
                }
            },
            sponsorData() {
                return {
                    labels: this.category_labels,
                    datasets: [{
                        data: this.s_values,
                        backgroundColor: this.s_values.map(() => this.randomizeColor())
                    }]
                }
            },
            sponsorOptions() {
                return {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: "Sponsor based on Industry"
                        },
                        legend: {
                            display: false,
                        }
                    },
                    scales: {
                        y: {
                            ticks: {
                                beginAtZero: true
                            },
                            scaleLabel: {
                                display: true,
                                labelString: "No. of Sponsor"
                            }
                        },
                        x: {
                            scaleLabel: {
                                display: true,
                                labelString: "Industry"
                            }
                        }
                    }
                }
            },
            influencerData() {
                return {
                    labels: this.category_labels,
                    datasets: [{
                        data: this.i_values,
                        backgroundColor: this.i_values.map(() => this.randomizeColor())
                    }]
                }
            },
            influencerOptions() {
                return {
                    plugins: {    
                        title: {
                            display: true,
                            text: "Influencer based on Niche"
                        },
                        legend: {
                            display: false,
                        }
                    },
                    scales: {
                        y: {
                            ticks: {
                                beginAtZero: true
                            },
                            scaleLabel: {
                                display: true,
                                labelString: "No. of Influencer"
                            }
                        },
                        x: {
                            scaleLabel: {
                                display: true,
                                labelString: "Niche"
                            }
                        }
                    }
                }
            }
        },
        created() {
            this.getDetails();
            this.getData();
        }
    }
</script>