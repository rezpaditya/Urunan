<script setup>
import { RouterView } from 'vue-router';
</script>

<template>
  <div class="flex flex-col h-screen min-h-screen">
    <div class="mb-auto">
      <RouterView />
    </div>
    
    <footer class="mt-auto">
      <div class="w-full mx-auto max-w-screen-xl p-4 md:flex md:items-center md:justify-between">
        <span class="text-sm text-gray-500 sm:text-center dark:text-gray-400">
          © 2024 Urunan |  
          <a href="https://github.com/rezpaditya/Urunan/actions">
            <img class="inline" src="https://github.com/rezpaditya/Urunan/actions/workflows/docker-deploy.yml/badge.svg" alt="Build Status"></a>
          </span>
      </div>
    </footer>
  </div>
</template>