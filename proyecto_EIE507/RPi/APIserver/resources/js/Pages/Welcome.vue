<script>
import { Head, Link } from '@inertiajs/inertia-vue3';
import Plotly from 'plotly.js-dist-min'
import axios from 'axios';

export default {
    components: {
        Head,
        Link,
        axios
    },

    props:{
        Scans: {
            type: Array,
            required: true,
        },
    },

    data() {
        return {
            datosSensor: null
        };
    },

    mounted() {
        this.datosSensor = this.Scans;
        this.getSensorData();

    },

    methods: {
        // Obtener datos del sensor cada 5 segundos
        async getSensorData() {
            await axios.get('/api/data/1')
            .then(response => {
                console.log(response.data['data']);
                this.datosSensor = response.data['data'];

                var trace1 = {
                x: this.datosSensor.map(function(e) {
                    return e.created_at_formatted;
                }),
                y: this.datosSensor.map(function(e) {
                    return e.amount;
                }),
                type: 'scatter'
                };        

                var data = [trace1];

                Plotly.newPlot('gd', data);

                setTimeout(this.getSensorData, 5000);
            });            
        }        
    }
};

</script>

<template>
    <Head title="EIE507 - PUCV" />

    <div class="relative flex items-top justify-center min-h-screen bg-gray-100 dark:bg-gray-900 sm:pt-0">
        <div v-if="canLogin" class="hidden fixed top-0 right-0 px-6 py-4 sm:block">
            <Link v-if="$page.props.user" :href="route('dashboard')" class="text-sm text-gray-700 dark:text-gray-500 underline">Dashboard</Link>

            <template v-else>
                <Link :href="route('login')" class="text-sm text-gray-700 dark:text-gray-500 underline">Log in</Link>

                <Link v-if="canRegister" :href="route('register')" class="ml-4 text-sm text-gray-700 dark:text-gray-500 underline">Register</Link>
            </template>
        </div>

        <div class="max-w-7xl mx-auto mt-16">
            <div id="logoContainer" class="w-full">
                <img id="logo" src="/asset/images/logo_pucv.png" alt="Logo" class="mx-auto" />
                <div class="text-white">
                    <p class="mb-4 text-center">
                        <span class="text-3xl block mb-8">Sistema de monitoreo de la calidad del aire</span>
                        Proyecto realizado para el curso EIE507 - Sistemas embebidos<br>
                        PUCV - EIE 2022
                        <br>
                    </p>

                    <div class="flex flex-row w-full justify-between">
                        <div>
                            <span class="text-green-400">Estudiantes:</span>
                            <ul class="text-pink-400 ml-4 mb-4">
                                <li class="list-disc">Jos?? Henr??quez Garnett</li>
                                <li class="list-disc">Juan Carlos Mu??oz</li>
                            </ul>                            
                        </div>
                        <div>
                            <span class="text-green-400">Profesor:</span>
                            <ul class="text-pink-400 ml-4">
                                <li class="list-disc">Sebasti??n Bruna</li>
                            </ul>
                        </div>
                    </div>

                    <div id="tablaDatos" class="my-8">
                        <!-- tabla con los datos del sensor -->
                        <table class="table-auto w-full">
                            <thead>
                                <tr>
                                    <th class="px-4 py-2">ID</th>
                                    <th class="px-4 py-2">Fecha</th>
                                    <th class="px-4 py-2">Lectura</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="dato in datosSensor" :key="dato.id">
                                    <td class="border px-4 py-2">{{ dato.id }}</td>
                                    <td class="border px-4 py-2">{{ dato.created_at_formatted }}</td>
                                    <td class="border px-4 py-2">{{ dato.amount }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div id="grafico">
                        <div id="gd"></div>
                    </div>
                </div>
            </div>            
        </div>
    </div>
</template>