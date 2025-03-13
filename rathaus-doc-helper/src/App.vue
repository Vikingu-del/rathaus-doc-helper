

<template>
  <div id="app">
    <!-- Sticky Navigation -->
    <header class="sticky-nav">
      <div class="logo">City of Wolfsburg</div>
      <nav>
        <ul>
          <li><a href="#">Home</a></li>
          <li><a href="#">Residents</a></li>
          <li><a href="#">Business Directory</a></li>
          <li><a href="#">Economic Development</a></li>
          <li><a href="#">City Government</a></li>
          <li><a href="#">Departments</a></li>
          <li><a href="#">Contact</a></li>
        </ul>
      </nav>
    </header>
    
    <div class="container">
      <h1>Welcome to the Rathaus Registration</h1>
      <form @submit.prevent="handleSubmit">
        <!-- This container is shown only if registration hasn't been answered -->
        <div v-if="isRegistered === null" class="containerButtons">
          <label>Are you already registered?</label>
          <button type="button" @click="handleRegistration(true)">Yes</button>
          <button type="button" @click="handleRegistration(false)">No</button>
        </div>
        
        <!-- Once an answer is provided the first container disappears -->
        <div v-if="isRegistered !== null" class="containerButtons">
          <label>Are you an EU citizen?</label>
          <button type="button" @click="handleCitizenship(true)">Yes</button>
          <button type="button" @click="handleCitizenship(false)">No</button>
        </div>
        
        <div v-if="isEU !== null">
          <label>Select a service:</label>
          <select v-model="selectedService">
            <option value="">Please select a service</option>
            <option value="residence">Application for Residence Permit</option>
            <option value="extension">Application for Extension of Residence Permit</option>
          </select>
        </div>

        <div v-if="isEU === true && selectedService">
          <label>Please scan your passport or ID:</label>
          <input type="file" @change="handleFileUpload" multiple />
        </div>

        <div v-if="isEU === false && selectedService">
          <label>Please scan your passport:</label>
          <input type="file" @change="handleFileUpload" multiple />
        </div>

        <div v-if="isEU !== null && selectedService && files.length">
          <button type="submit">Submit</button>
        </div>
      </form>
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
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  overflow-x: hidden;
  font-family: Arial, sans-serif;
}

.sticky-nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: #004d00;
  color: white;
  display: flex;
  justify-content: flex-start;
  padding: 1rem;
  z-index: 1000;
}

.sticky-nav .logo {
  font-size: 1.5rem;
  font-weight: bold;
  padding-right: 5%;
}

.sticky-nav nav ul {
  list-style: none;
  display: flex;
  gap: 1rem;
  margin: 0;
  padding: 0;
}
.sticky-nav nav ul {
  list-style: none;
  display: flex;
  gap: 2rem;
  margin: 0;
  padding: 0;
}
.sticky-nav nav ul li a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.container {
  padding: 7rem 5% 2rem;
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
  width: 100vw;

}

.containerButtons {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
  overflow-y : hidden;

  width: 100%;

}

.containerButtons label {
  margin-bottom: 25px;
  font-weight: bold;
  font-size: 1.2em;

}

.containerButtons .button-group {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 600px; /* Controls how far apart the buttons can get */
  
}

.containerButtons .button-group button {
  padding: 1.5em 3.5em;
  font-size: 14px;
  min-width: 150px;
  margin: 0.6rem 1rem;
  font-weight: bold;
  
}

/* You can also style the buttons container specifically */
.containerButtons .button-group {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  
}



button {
  margin: 0.6rem;
  padding: 0.6rem 1rem;
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
button {
  padding: 1.3em 3em;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  font-weight: 500;
  color: #000;
  background-color: #fff;
  border: none;
  border-radius: 45px;
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease 0s;
  cursor: pointer;
  outline: none;
}

button:hover {
  background-color: #23c483;
  box-shadow: 0px 15px 20px rgba(46, 229, 157, 0.4);
  color: #fff;
  transform: translateY(-7px);
}

button:active {
  transform: translateY(-1px);
}

input[type="file"], select {
  margin: 0.6rem;
  padding: 0.5rem;
  width: 100%;
  max-width: 400px;
  
}

@media (max-width: 768px) {
  .sticky-nav {
    flex-direction: column;
    align-items: center;
  }

  @media (max-width: 500px) {
  .containerButtons .button-group {
    flex-direction: column;
    align-items: center;
  }
}
  
  .sticky-nav nav ul {
    flex-direction: column;
    align-items: center;
    margin-top: 1rem;
    
  }
  
  .container {
    padding-top: 9rem;
    
  }
}
</style>
