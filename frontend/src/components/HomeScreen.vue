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
               tweets: [
                    {
                         "id": 1026814183042687000,
                         "date": "Tue Aug 07 12:55:53 +0000 2018",
                         "text": "RT @de_patty: Asuuuuuuu..  @Renzo_Reggiardo me da mala espina...su pasado fujimorísta qué miedo!!!y @luchocastanedap hijo de corrupto que s…",
                         "user_id": 544008122,
                         "user_name": "@CARLOSPUEMAPE1",
                         "location": {},
                         "retweeted": true,
                         "RT_text": "Asuuuuuuu..  @Renzo_Reggiardo me da mala espina...su pasado fujimorísta qué miedo!!!y @luchocastanedap hijo de corrupto que secunda lo del padre NI HABLAR! Más comunicore Plop!lideran las preferencias para la alcaldía de Lima, según Ipsos | RPP Noticias https://t.co/w5TnU0Dmwq",
                         "RT_user_id": 302995560,
                         "RT_user_name": "@de_patty"
                    },
                    {
                         "id": 1026814466145628200,
                         "date": "Tue Aug 07 12:57:00 +0000 2018",
                         "text": "@JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @MunozaLima @AccionColorao Que gracioso este candidato. Ese día fue escueliado por los #JovenesK y ahora saca su meme. 😆   https://t.co/ztqu20KAuF",
                         "user_id": 831616598083588100,
                         "user_name": "@JovenesConFP",
                         "location": {},
                         "retweeted": false
                    },
                    {
                         "id": 1026815522997002200,
                         "date": "Tue Aug 07 13:01:12 +0000 2018",
                         "text": "@de_patty @Renzo_Reggiardo @luchocastanedap Y estos patitas son más conchudos que sus viejos,con tan sólo decir eso fue en el tiempo de mi padre,tapan todo,más de mismo.",
                         "user_id": 132649817,
                         "user_name": "@cefp01",
                         "location": {},
                         "retweeted": false
                    },
                    {
                         "id": 1026815774055452700,
                         "date": "Tue Aug 07 13:02:12 +0000 2018",
                         "text": "RT @de_patty: Asuuuuuuu..  @Renzo_Reggiardo me da mala espina...su pasado fujimorísta qué miedo!!!y @luchocastanedap hijo de corrupto que s…",
                         "user_id": 170830041,
                         "user_name": "@vladynz",
                         "location": {},
                         "retweeted": true,
                         "RT_text": "Asuuuuuuu..  @Renzo_Reggiardo me da mala espina...su pasado fujimorísta qué miedo!!!y @luchocastanedap hijo de corrupto que secunda lo del padre NI HABLAR! Más comunicore Plop!lideran las preferencias para la alcaldía de Lima, según Ipsos | RPP Noticias https://t.co/w5TnU0Dmwq",
                         "RT_user_id": 302995560,
                         "RT_user_name": "@de_patty"
                    },
                    {
                         "id": 1026816089110601700,
                         "date": "Tue Aug 07 13:03:27 +0000 2018",
                         "text": "RT @MikeReategui: #HablaCastañeda https://t.co/fRmACwQ06D",
                         "user_id": 62131246,
                         "user_name": "@mundoyola",
                         "location": {},
                         "retweeted": true,
                         "RT_text": "#HablaCastañeda https://t.co/fRmACwQ06D",
                         "RT_user_id": 41526072,
                         "RT_user_name": "@MikeReategui"
                    },
                    {
                         "id": 1026816185126596600,
                         "date": "Tue Aug 07 13:03:50 +0000 2018",
                         "text": "@JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @MunozaLima @AccionColorao Que bajo puede caer un candidato. Aprovecharse de un encuentro casual para hacer un meme. Esto dice mucho de Ud. que utiliza a el Gringo K. y se aprovecha de los Jóvenes de Fuerza Popular que democráticamente le de volvieron el saludo cuando USTED se acercó.",
                         "user_id": 66786769,
                         "user_name": "@lulavitz",
                         "location": {},
                         "retweeted": false
                    },
                    {
                         "id": 1026816558876844000,
                         "date": "Tue Aug 07 13:05:19 +0000 2018",
                         "text": "@JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @MunozaLima @AccionColorao Que maricon para hacer este tipo de meme y asi quiere ser Alcalde señor Muñoz engañando a la población, jugando con la buena voluntad d la juventud?, es una lastima , tenia que se de Acción Popular",
                         "user_id": 1020629868,
                         "user_name": "@_CorazonSalvaj",
                         "location": {},
                         "retweeted": false
                    },
                    {
                         "id": 1026816984787443700,
                         "date": "Tue Aug 07 13:07:01 +0000 2018",
                         "text": "@RecuerdosPeru @Renzo_Reggiardo @RenzopeOficial @LuchoCastanedaL \"Los Intocables Ediles forman parte de “La mancha amarilla”, una red de burgomaestres delincuentes catapultados por dos agrupaciones políticas: Solidaridad Nacional de Luis Castañeda Lossio y Podemos Perú de José Luna Gálvez.\" OJO #DecideBien",
                         "user_id": 442247879,
                         "user_name": "@liliana2sd",
                         "location": {},
                         "retweeted": false
                    },
                    {
                         "id": 1026817603191357400,
                         "date": "Tue Aug 07 13:09:28 +0000 2018",
                         "text": "@_CorazonSalvaj @JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @MunozaLima @AccionColorao Hacer una broma de un encuentro entre dos partidos que se saludaron educadamente, es lamentable. Usted no tiene ética. Los jóvenes no cambiamos el voto. Usted es un mentiroso.",
                         "user_id": 881380951,
                         "user_name": "@Clauditaato",
                         "location": {},
                         "retweeted": false
                    },
                    {
                         "id": 1026817611626172400,
                         "date": "Tue Aug 07 13:09:30 +0000 2018",
                         "text": "@JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @MunozaLima @AccionColorao Lo cortes no quita lo valiente y una de los principales valores inculcados en los jovenes de Fuerza Popular es ser amable con quien se cruce en nuestro camino y hacer que la población vea q en el Partido FUERZA  POPULAR siempre nuestro actuar es con amabilidad y no odio.",
                         "user_id": 890311782509707300,
                         "user_name": "@JudithNancy69",
                         "location": {},
                         "retweeted": false
                    },
                    {
                         "id": 1026818103135621100,
                         "date": "Tue Aug 07 13:11:27 +0000 2018",
                         "text": "@JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @MunozaLima @AccionColorao Le sugiero un debate con Ditel Columbus y verá como le borrará su sonrisa y su rostro será de admiración hacia él. Vamos Ditel Vamos Hasta la Alcaldia no paramos..!!!",
                         "user_id": 890311782509707300,
                         "user_name": "@JudithNancy69",
                         "location": {},
                         "retweeted": false
                    },
                    {
                         "id": 1026819148486246400,
                         "date": "Tue Aug 07 13:15:37 +0000 2018",
                         "text": "@DanielUrresti1 Es que Phillip Butter es de la señora K , así de simple señores",
                         "user_id": 987371563329572900,
                         "user_name": "@Jorge31574555",
                         "location": {},
                         "retweeted": false
                    },
                    {
                         "id": 1026819193428226000,
                         "date": "Tue Aug 07 13:15:47 +0000 2018",
                         "text": "@de_patty @Renzo_Reggiardo @luchocastanedap Después se quejan de los políticos... el gran problema no es que sean delincuentes o con pasado oscuro, lo que realmente preocupa es cómo son elegidos por el pueblo. Si seguimos así, no nos quejemos del congreso ni de los presidentes... va a seguir siendo lo mismo.",
                         "user_id": 1277728950,
                         "user_name": "@Gianfranco_mna",
                         "location": {},
                         "retweeted": false
                    },
                    {
                         "id": 1026819287632232400,
                         "date": "Tue Aug 07 13:16:10 +0000 2018",
                         "text": "RT @comentarista196: @DanielUrresti1 El camaleón de la política es Candidato de FP: https://t.co/cjjDGsmz2u",
                         "user_id": 987371563329572900,
                         "user_name": "@Jorge31574555",
                         "location": {},
                         "retweeted": true,
                         "RT_text": "@DanielUrresti1 El camaleón de la política es Candidato de FP: https://t.co/cjjDGsmz2u",
                         "RT_user_id": 2612839550,
                         "RT_user_name": "@comentarista196"
                    },
                    {
                         "id": 1026819476900274200,
                         "date": "Tue Aug 07 13:16:55 +0000 2018",
                         "text": "RT @lulavitz: @JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @MunozaLima…",
                         "user_id": 134959308,
                         "user_name": "@PIP1509",
                         "location": {},
                         "retweeted": true,
                         "RT_text": "@JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @MunozaLima @AccionColorao Que bajo puede caer un candidato. Aprovecharse de un encuentro casual para hacer un meme. Esto dice mucho de Ud. que utiliza a el Gringo K. y se aprovecha de los Jóvenes de Fuerza Popular que democráticamente le de volvieron el saludo cuando USTED se acercó.",
                         "RT_user_id": 66786769,
                         "RT_user_name": "@lulavitz"
                    },
                    {
                         "id": 1026819483938291700,
                         "date": "Tue Aug 07 13:16:57 +0000 2018",
                         "text": "@Viankagvp @DanielUrresti1 Jajajajajajaja... Así es señora, si mi madrina fuera la señora K, hace tiempo ya fuera CONGRESISTA o alcalde.",
                         "user_id": 987371563329572900,
                         "user_name": "@Jorge31574555",
                         "location": {},
                         "retweeted": false
                    },
                    {
                         "id": 1026819502925918200,
                         "date": "Tue Aug 07 13:17:01 +0000 2018",
                         "text": "RT @AndradeTovarA: @JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @Munoz…",
                         "user_id": 134959308,
                         "user_name": "@PIP1509",
                         "location": {},
                         "retweeted": true,
                         "RT_text": "@JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @MunozaLima @AccionColorao Tío gracioso! Tu te acercaste y todo termino en burla, los jóvenes jamas cambiamos nuestro voto por que se acerque un rato un candidato NN, rectifica tu tweet",
                         "RT_user_id": 3302963577,
                         "RT_user_name": "@AndradeTovarA"
                    },
                    {
                         "id": 1026819552603238400,
                         "date": "Tue Aug 07 13:17:13 +0000 2018",
                         "text": "RT @JovenesConFP: @JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @Munoza…",
                         "user_id": 134959308,
                         "user_name": "@PIP1509",
                         "location": {},
                         "retweeted": true,
                         "RT_text": "@JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @MunozaLima @AccionColorao Que gracioso este candidato. Ese día fue escueliado por los #JovenesK y ahora saca su meme. 😆   https://t.co/ztqu20KAuF",
                         "RT_user_id": 831616598083588100,
                         "RT_user_name": "@JovenesConFP"
                    },
                    {
                         "id": 1026819588498120700,
                         "date": "Tue Aug 07 13:17:21 +0000 2018",
                         "text": "RT @_CorazonSalvaj: @JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @Muno…",
                         "user_id": 134959308,
                         "user_name": "@PIP1509",
                         "location": {},
                         "retweeted": true,
                         "RT_text": "@JorgeMunozAP @ap_bancada @AccionPopularPe @AccionPopular @AccionPopularAP @ppdenaccion @AccionPopularLo @APJOVEN @MunozaLima @AccionColorao Que maricon para hacer este tipo de meme y asi quiere ser Alcalde señor Muñoz engañando a la población, jugando con la buena voluntad d la juventud?, es una lastima , tenia que se de Acción Popular",
                         "RT_user_id": 1020629868,
                         "RT_user_name": "@_CorazonSalvaj"
                    },
                    {
                         "id": 1026820067730841600,
                         "date": "Tue Aug 07 13:19:16 +0000 2018",
                         "text": "RT @Gianfranco_mna: @de_patty @Renzo_Reggiardo @luchocastanedap Después se quejan de los políticos... el gran problema no es que sean delin…",
                         "user_id": 970808047701516300,
                         "user_name": "@mizp0890",
                         "location": {},
                         "retweeted": true,
                         "RT_text": "@de_patty @Renzo_Reggiardo @luchocastanedap Después se quejan de los políticos... el gran problema no es que sean delincuentes o con pasado oscuro, lo que realmente preocupa es cómo son elegidos por el pueblo. Si seguimos así, no nos quejemos del congreso ni de los presidentes... va a seguir siendo lo mismo.",
                         "RT_user_id": 1277728950,
                         "RT_user_name": "@Gianfranco_mna"
                    },
               ],
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
                    // TODO: if response was successful, then set flag to false and tell user
                    // file was uplaoded sucessfully
                    console.log("UPLOAD FILE RESPONSE: " + response);
               }).catch(() => {
                    console.log("error occurred when uploading a file");
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
                    // this.tweets = response.tweets;
                    this.processingQuery = false;
               }).catch(() => {
                    console.log("error occurred when processing query");
               });

               // send query to server and process response
               this.query = 'Procesando query...';
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