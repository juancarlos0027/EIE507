<script setup>
import { Head, Link } from '@inertiajs/inertia-vue3';

defineProps({
    canLogin: Boolean,
    canRegister: Boolean,
    laravelVersion: String,
    phpVersion: String,
});
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
                </div>
            </div>            
        </div>
    </div>
</template>