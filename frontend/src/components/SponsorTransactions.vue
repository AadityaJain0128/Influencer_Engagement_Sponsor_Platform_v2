<template>
    <div id="container">
        <div id="transactions" class="m-5">
            <h1 align="center">Transactions</h1>
            <div id="download_csv" align="right" class="mb-2">
                <button type="submit" class="btn btn-dark" @click="downloadCSV">Download</button>
            </div>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">Transaction<br>ID</th>
                        <th scope="col">Campaign<br>Name</th>
                        <th scope="col">Influencer</th>
                        <th scope="col">Pay Amount</th>
                        <th scope="col">Date</th>
                        <th scope="col">Time</th>
                        <th scope="col">Campaign<br>Details</th>
                    </tr>
                </thead>
                <tbody v-if="transactions.length > 0">
                    <tr v-for="t in transactions" :key="t.id">
                        <td>{{ t.id }}</td>
                        <td>{{ t.campaign.name }}</td>
                        <td>{{ t.influencer.name }} (@{{ t.influencer.username }})</td>
                        <td>INR {{ t.amount }}</td>
                        <td>{{ t.date }}</td>
                        <td>{{ t.time }}</td>
                        <td><router-link :to="'/campaigns/' + t.campaign.id" class="btn btn-outline-dark">View</router-link></td>
                    </tr>
                </tbody>
                <tbody v-else>
                    <tr>
                        <td align="center" rowspan="2" colspan="7">No Transactions !</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>


<script>
    export default {
        name : "SponsorTransactions",
        data() {
            return {
                transactions : []
            }
        },
        methods : {
            async getTransactions() {
                let { data } = await this.$http.get("/sponsor/transactions", {
                    headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` }
                });

                if (data.status == "success") {
                    this.transactions = data.transactions;
                }
            },

            downloadCSV() {
                let csvContent = this.convertToCSV(this.transactions);
                let blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
                let link = document.createElement("a");
                link.href = URL.createObjectURL(blob);
                link.download = "transactions.csv";
                link.click();
            },

            convertToCSV(data) {
                let header = ["Transaction ID", "Campaign", "Influencer", "Pay Amount", "Date", "Time"];
                let rows = data.map(t => {
                    return [
                        t.id,
                        t.campaign.name,
                        `${t.influencer.name} (@${t.influencer.username})`,
                        t.amount,
                        t.date,
                        t.time
                    ]
                    .map(value => `"${value}"`).join(',')}).join('\n');
                return header.join(',') + '\n' + rows;
            }

        },
        created() {
            this.getTransactions();
        }
    }
</script>