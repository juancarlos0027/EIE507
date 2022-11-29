<script>
import { Head, Link } from '@inertiajs/inertia-vue3';
import { Chart } from 'chart.js/auto'

export default {
    components: {
        Head,
        Link,
        Chart
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
    
        const chartAreaBorder = {
            id: 'chartAreaBorder',

            beforeDraw(chart, args, options) {
            const { ctx, chartArea: { left, top, width, height } } = chart;

            ctx.save();
            ctx.strokeStyle = options.borderColor;
            ctx.lineWidth = options.borderWidth;
            ctx.setLineDash(options.borderDash || []);
            ctx.lineDashOffset = options.borderDashOffset;
            ctx.strokeRect(left, top, width, height);
            ctx.restore();
            }
        };

        new Chart(
        document.getElementById('graficaSensor'),
        {
        type: 'line',
        plugins: [chartAreaBorder],
        options: {
            plugins: {
                chartAreaBorder: {
                    borderColor: '#FFFFFF',
                    borderWidth: 2,
                    borderDash: [5, 5],
                },
            },            
        },
        data: {
            labels: this.datosSensor.map(dato => dato.created_at),
            datasets: [
            {
                label: 'Lectura del sensor (PPM de CO)',
                data: this.datosSensor.map(dato => dato.amount)
            }
            ]
        }
        }
    );
    },
};

</script>

<template>
    <Head title="Welcome" />

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
                                <li class="list-disc">José Henríquez Garnett</li>
                                <li class="list-disc">Juan Carlos Muñoz</li>
                            </ul>                            
                        </div>
                        <div>
                            <span class="text-green-400">Profesor:</span>
                            <ul class="text-pink-400 ml-4">
                                <li class="list-disc">Sebastián Bruna</li>
                            </ul>
                        </div>
                    </div>

                    <div id="grafico">
                        <canvas id="graficaSensor" width="400" height="400"></canvas>
                    </div>
                </div>
            </div>            
        </div>
    </div>
</template>