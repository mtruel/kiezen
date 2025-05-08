<template>
  <div class="mt-8 flex relative lg:mt-0 lg:py-4 lg:pl-[calc(var(--section-gap)/2)]">
    <i class="flex place-items-center place-content-center w-8 h-8 text-gray-600 lg:absolute lg:top-[calc(50%-25px)] lg:-left-[26px] lg:w-[50px] lg:h-[50px] lg:border lg:border-gray-200 lg:bg-white lg:rounded-lg">
      <slot name="icon"></slot>
    </i>
    <div class="flex-1 ml-4">
      <h3 class="text-xl font-medium mb-1.5 text-gray-900">
        <slot name="heading"></slot>
      </h3>
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
/* Remove all custom CSS as we're using Tailwind now */
</style>
