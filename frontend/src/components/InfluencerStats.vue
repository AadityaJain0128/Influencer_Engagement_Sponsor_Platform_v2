<template>
    <div id="container">
        <h1 align="center" class="mb-5">Statistics</h1>
        <div style="width: 50%; float: left;">
            <h3 class="d-flex justify-content-center">Campaigns</h3>
            <div v-if="total_campaigns > 0">
                <Pie :data="campaignData" :options="campaignOptions" style="width: 100%; max-height: 400px; max-width: 700px;"></Pie>
                <br>
                <div align="center"><span>Total Campaigns<br>{{ total_campaigns }}</span></div>
            </div>
            <div v-else class="d-flex justify-content-center">No Data to display !</div>
        </div>
        <div style="width: 50%; float: left;">
            <h3 class="d-flex justify-content-center">Transactions</h3>
            <div v-if="averagePay > 0">
                <Bar :data="transactionData" :options="transactionOptions" style="width: 100%; max-height: 400px; max-width: 700px;"></Bar>
                <br>
                <div align="center">
                    <span>
                        Average Pay Amount
                        <br>
                        INR {{ averagePay }}
                    </span>
                </div>    
            </div>
            <div v-else class="d-flex justify-content-center">No Data to Display !</div>
        </div>
    </div>
</template>

<script>
    import { Pie, Bar } from 'vue-chartjs';
    import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js';

    ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);

    export default {
        name : "InfluencerStats",
        components : {
            Pie, Bar
        },
        data() {
            return {
                campaign_labels : [],
                campaign_values : [],
                campaign_colors : ["green", "blue"],
                transaction_labels : [],
                transaction_values : []
            }
        },
        computed: {
            campaignData() {
                return {
                    labels: this.campaign_labels,
                    datasets: [{
                        data: this.campaign_values,
                        backgroundColor: this.campaign_colors
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
            total_campaigns() {
                return this.campaign_values.reduce((a, b) => a + b, 0);
            },
            averagePay() {
                return this.transaction_values.length == 0 ? 0 : (this.transaction_values.reduce((a, b) => a + b, 0) / this.transaction_values.length).toFixed(2)
            }
        },
        methods : {
            async getData() {
                let { data } = await this.$http.get("/influencer/stats", {
                    headers : { Authorization : `Bearer ${this.$store.getters.authToken}` }
                });

                if (data.status == "success") {
                    this.campaign_labels = data.campaign_labels;
                    this.campaign_values = data.campaign_values;
                    this.transaction_labels = data.transaction_labels;
                    this.transaction_values = data.transaction_values;
                }
            },
            randomizeColor() {
                let hex = "0123456789ABCDEF";
                let color_code = "#";
                for (let i = 0; i < 6; i++) {
                    color_code += hex[parseInt(Math.random() * 16)]
                }
                return color_code
            }
        },
        created() {
            this.getData();
        }
    }
</script>