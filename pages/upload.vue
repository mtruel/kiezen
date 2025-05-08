<script lang="ts" setup>
const toUploadFiles = ref<File[]>([])


const handleFileChange = (files: File[]) => {
  toUploadFiles.value = files
}


const submit = async () => {
  console.log("Uploading", toUploadFiles.value);
  if (!toUploadFiles.value || toUploadFiles.value.length === 0) {
    console.error('No files to upload');
    return;
  }

  for (let i = toUploadFiles.value.length - 1; i >= 0; i--) {
    const formData = new FormData();
    const file = toUploadFiles.value[i];
    formData.append('file', file); // Use 'file' as key (as shown in the curl example)

    try {
      const response = await $fetch('/api/v1/uploadfile', {
        method: 'POST',
        body: formData,
        headers: {
          accept: 'application/json', // Ensure server returns JSON response
        },
      });

      if (!response) return;

      toUploadFiles.value.splice(i, 1);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert(`Failed to upload the file. ${error}`)
    }
  }


}
</script>

<template>
  <!--  <div class="flex flex-col items-center">-->
  <div class="flex flex-col items-center justify-center">
    <InteractiveHoverButton v-if="toUploadFiles.length" text="Submit" @click="submit"/>
  </div>
  <FileUpload @onChange="handleFileChange"/>
  <!--  </div>-->
</template>

<style scoped>

</style>