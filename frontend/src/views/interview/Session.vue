<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="bg-white rounded-lg shadow">
      <div class="px-4 py-5 sm:p-6">
        <h2 class="text-lg font-medium text-gray-900">Interview Session {{ $route.params.id }}</h2>
        <p class="mt-2 text-gray-600">This is a mock interview session page.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InterviewSession'
}
</script>