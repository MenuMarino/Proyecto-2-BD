<template>
  <div id="container">
       <div id="inputs" class="super-item">
          <div id="query-section" class="item">
               <h2>Query</h2>
               <input type="text" v-model="query" placeholder="Buscar tweets...">
               <button v-on:click="processQuery()">Buscar</button>
               <p>Query: {{ query }}</p>
               <div v-if="processingQuery">
                    <h3>Processing Query...</h3>
               </div>
          </div>
          <div lass="item">
               <h2>Filter Query Results</h2>
               <input type="text" v-model="filterResult" placeholder="Filtrar tweets...">
               <p>Filter: {{filterResult}}</p>
          </div>
          <div id="file-section" class="item">
               <h2>Archivo para Indexar</h2>
               <input type="file" name="file" v-on:change="prepareToUploadFile($event.target.name, $event.target.files)">
               <button v-on:click="uploadFile()">Index File</button>
               <p>File: {{ this.selectedFiles != null ? this.selectedFiles : 'No se ha seleccionado un archivo' }}</p>
               <div v-if="processingFile">
                    <h3>Indexing file...</h3>
               </div>
          </div>
       </div>
       <div id="query-results" class="super-item" v-for="tweet in filterTweets" v-bind:key="tweet.id">
            <div class="tweet-container">
                 <p><strong>ID:</strong> {{ tweet.id }}</p>
                 <p><strong>Date:</strong> {{ tweet.date.substr(0, 19) }}</p>
                 <p><strong>Text:</strong> {{ tweet.text }}</p>
                 <p><strong>User ID:</strong> {{ tweet.user_id }}</p>
                 <p><strong>Username:</strong> {{ tweet.user_name }}</p>
                 <!-- TODO: location -->
                 <div v-if="tweet.retweeted">
                      <p><strong>Retweet Text:</strong> {{ tweet.RT_text }}</p>
                      <p><strong>Retweet User ID:</strong> {{ tweet.RT_user_id }}</p>
                      <p><strong>Retweet Username:</strong> {{ tweet.RT_user_name }}</p>
                 </div>
            </div>
       </div>
  </div>
</template>

<script>

// TODO: mandar el 'k' de los k mas cercanos

import axios from 'axios';
import filterTweetsMixin from '../mixins/filterTweetsMixin';

export default {
     name: 'HomeScreen',
     data() {
          return {
               query: '',
               archivo: null,
               selectedName: '',
               selectedFiles: [],
               filterResult: '',
               processingQuery: false,
               processingFile: false,
               tweets: [],
          }
     },
     created() {
          console.log("component was created");
     },
     mixins: [
          filterTweetsMixin
     ],
     methods: {
          uploadFile() {
               // TODO: send file to server
               console.log(`NAME: ${this.selectedName}`);
               console.log(`FILES: ${this.selectedFiles[0]}`);
               // TODO: show "Loading..." while server is indexing file
               this.processingFile = true;

               // TODO: send multipart reuqest and set flag to false when response finished
               let formData = new FormData();

               formData.append('file', this.selectedFiles[0]);

               axios.post(
                    'http://127.0.0.1:5000/uploadFile',
                    formData,
                    {
                         headers: {
                              'Content-Type': 'multipart/form-data',
                              'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
                         }
                    }
               ).then((response) => {
                    console.log("UPLOAD FILE RESPONSE: " + response);
                    this.processingFile = false;
               }).catch(() => {
                    console.log("error occurred when uploading a file");
                    this.processingFile = false;
               });

          },
          prepareToUploadFile(name, files) {
               if (files.length === 0) {
                    // show alert saying no file was chosen
                    console.log("Need one file to index.");
                    return;
               }
               this.selectedName = name;
               this.selectedFiles = files;
          },
          processQuery() {
               if (this.query === '') {
                    // show alert saying cannot process empty query
                    console.log("Cannot process empty query.");
                    return;
               }

               this.processingQuery = true;

               // TODO: mandar le un url paremeter con el 'this.query'
               axios.get(
                    `http://127.0.0.1:5000/queryTweets?query=${this.query}`,
                    {
                         headers: {
                              'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
                         }
                    }
                    ).then( (response) => {
                    console.log("QUERY TWEETS RESPONSE:");
                    console.log(response);
                    if (typeof response.data !== 'undefined') {
                         this.tweets = response.data;
                    }
                    this.processingQuery = false;
               }).catch(() => {
                    console.log("error occurred when processing query");
               });
          },
     },
}
</script>

<style>

     #inputs {
          display: flex;
          justify-content: space-evenly;
     }

     #query-results {
          display: flex;
          flex-direction: column;
          margin: 1%;
     }

     .tweet-container {
          flex-basis: 50%;
          border-color: black;
          border-style: solid;
     }

</style>