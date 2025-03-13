<template>
  <div id="app">
    <h1>Welcome to the Rathaus Registration</h1>
    <form @submit.prevent="handleSubmit">
      <!-- Registration Status -->
      <div>
        <label>Are you already registered?</label>
        <button type="button" @click="handleRegistration(true)">Yes</button>
        <button type="button" @click="handleRegistration(false)">No</button>
      </div>

      <!-- EU Citizenship Question -->
      <div v-if="isRegistered !== null">
        <label>Are you an EU citizen?</label>
        <button type="button" @click="handleCitizenship(true)">Yes</button>
        <button type="button" @click="handleCitizenship(false)">No</button>
      </div>

      <!-- Service Selection -->
      <div v-if="isEU !== null">
        <label>Select a service:</label>
        <select v-model="selectedService">
          <option value="">Please select a service</option>
          <option value="residence">Aplication for Residence Permit</option>
          <option value="extension">Aplication for Extension of Residence Permit</option>
        </select>
      </div>

      <!-- Document Upload for EU Citizens -->
      <div v-if="isEU === true && selectedService">
        <label>Please scan your passport or ID:</label>
        <input type="file" @change="handleFileUpload" multiple />
      </div>

      <!-- Document Upload for Non-EU Citizens -->
      <div v-if="isEU === false && selectedService">
        <label>Please scan your passport:</label>
        <input type="file" @change="handleFileUpload" multiple />
      </div>

      <!-- Submit Button -->
      <div v-if="isEU !== null && selectedService && files.length">
        <button type="submit">Submit</button>
      </div>
    </form>

    <div v-if="formData">
      <h3>Form Submitted:</h3>
      <pre>{{ formData }}</pre>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isRegistered: null,    // null: not decided, true: yes, false: no
      isEU: null,           // null: not decided, true: EU, false: Non-EU
      selectedService: '',   // Selected service
      files: [],            // Array to hold uploaded files
      formData: null        // Holds the submitted form data for preview
    };
  },
  methods: {
    handleRegistration(status) {
      this.isRegistered = status;
    },
    handleCitizenship(status) {
      this.isEU = status;
    },
    handleFileUpload(event) {
      this.files = event.target.files;
    },
    async handleSubmit() {
      try {
        const formData = new FormData();
        
        formData.append('formData', JSON.stringify({
          isRegistered: this.isRegistered,
          isEU: this.isEU,
          selectedService: this.selectedService
        }));

        Array.from(this.files).forEach(file => {
          formData.append('files', file);
        });

        this.isSubmitting = true;

        const response = await fetch('/api/submitData', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        this.formData = result;
        alert('Documents submitted successfully!');

      } catch (error) {
        console.error('Submission error:', error);
        alert('Error submitting documents. Please try again.');
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin-top: 50px;
}

form {
  margin-top: 20px;
  text-align: center;
}

button {
  margin: 10px;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

button:disabled {
  background-color: gray;
  cursor: not-allowed;
}

input[type="file"], select {
  margin: 10px;
  padding: 5px;
  width: 200px;
}

select {
  height: 35px;
  border-radius: 5px;
  border: 1px solid #ccc;
}
</style>
