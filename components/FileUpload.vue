<script setup lang="ts">
const {handleFileInput, files} = useFileStorage({clearOldFiles: true})

const fileInput = ref<HTMLInputElement>()

const handleDrop = (e: any) => {
  // alert(
  //     'drag and drop functionality does not work currently, you can try to fix it in the repo :)',
  // )
  // console.log(e.dataTransfer.files[0]);s

  e.preventDefault()
  e.target.classList.remove("drag-active")
  if (fileInput.value) return
  // files.value = e.dataTransfer.files
  // console.log(e.dataTransfer.files, files.value);
  const e2 = {target: {files: e.dataTransfer.files}};
  handleFileInput(e2);
  // files.value = e.dataTransfer.files;
  // alert(fileInput.value.dispatchEvent(new Event("change event for file", {})))

  console.log("Files", files.value);
}

const fileLinks = ref<string[]>([])
const approveUpload = ref('')

const submit = async () => {
  const response = await $fetch('/api/v1/files', {
    method: 'POST',
    body: {
      files: files.value,
    },
  })
  if (!response) return
  approveUpload.value = 'Uploaded files successfully!'
  // fileLinks.value = response
}
</script>

<template>
  <<!--  <div class="flex flex-col items-center justify-center w-full h-screen gap-4 font-mono">-->
  <!--    <header class="flex items-center gap-8">-->
  <!--      <img src="/cover.png" alt="" class="w-20 animate-bounce"/>-->
  <!--      <h1 class="text-4xl">-->
  <!--        <span-->
  <!--            class="bg-gradient-to-r from-green-400 via-green-500 to-green-700 bg-clip-text text-transparent">Nuxt</span>-->
  <!--        Storage-->
  <!--      </h1>-->
  <!--    </header>-->
  <!--    <div class="flex h-80 w-full">-->>
  <div class="flex flex-col items-center gap-4">
    <div class="grid gap-4 my-4">
      <a v-for="link in fileLinks" :key="link" :href="`/userFiles/specificFolder/${link}`"
         class="px-4 py-2 bg-green-200 rounded-md text-black no-underline">{{ link }}</a>
    </div>
    <label
        id="dropcontainer"
        for="images"
        class="drop-container relative flex flex-col justify-center items-center w-11/12 p-5 rounded-lg border-2 border-dashed border-gray-500 text-gray-600 cursor-pointer hover:bg-gray-100 hover:border-black transition-all"
        @dragover.prevent
        @dragenter.prevent="(e: any) => {e.target.classList.add('drag-active')}"
        @dragleave.prevent="(e: any) => {e.target.classList.remove('drag-active')}"
        @drop.prevent="handleDrop"
    >
      <span class="text-lg font-bold text-gray-600 transition-color">Drop files here</span>
      or
      <input
          id="file-input"
          ref="fileInput"
          type="file"
          name="files[]"
          multiple
          @input="handleFileInput"
          @click="approveUpload == ''"
          class="mt-2"
      />
    </label>
    <button @click="submit" class="bg-green-200 py-2 px-4 rounded-md text-black hover:bg-green-400 transition-all">
      Submit
    </button>
    <p class="flex-wrap"> {{ files }}</p>
    <p>{{ approveUpload }}</p>
  </div>
  <!--  </div>-->
  <!--  </div>-->
  <!--  <input type="file" @input="handleFileInput"/>-->
  <!--  <button @click="submit">submit</button>-->
</template>

