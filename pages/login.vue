<script lang="ts" setup>
const loginUser = () => {
  const isAuthenticated = useAuthentication();
  console.log('User is now authenticated:', isAuthenticated.value);
  navigateTo('/library');
};
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="p-10 bg-white rounded shadow">
      <h1 class="mb-5 text-lg font-bold">Login Page</h1>
      <UButton color="primary" @click="loginUser">Login</UButton>
    </div>
  </div>
</template>

<style scoped>

</style>