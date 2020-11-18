#define pin_accensione_laser 4
#define time_segnale_lungo 100
#define time_segnale_corto 50
#define time_pausa_tra_segnali 50

void setup() {
  pinMode(pin_accensione_laser, OUTPUT);
  Serial.begin(9600);
  Serial.println("inserisci stringa:");
}

void loop() {
  if(Serial.available()){
    char ch = Serial.read();

    if((ch=='\n') || (ch=='\r')){
      
    }else{
      Serial.println(ch);
      process(ch);
    }

}
}

void process(char ch){
    switch(ch){
      case '0':
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      break;
      case '1':
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      break;
      case '2':
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      break;
      case '3':
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      break;
      case '4':
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      break;
      case '5':
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      break;
      case '6':
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      break;
      case '7':
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleCorto();
      break;
      case '8':
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      break;
      case '9':
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      break;
      case 'a':
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      break;
      case 'b':
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      break;
      case 'c':
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      break;
      case 'd':
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      break;
      case 'e':
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      break;
      case 'f':
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleCorto();
      segnaleCorto();
      break;
      case 'g':
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      break;
      case 'h':
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      break;
      case 'i':
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      break;
      case 'j':
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      break;
      case 'k':
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      break;
      case 'l':
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      break;
      case 'm':
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      break;
      case 'n':
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleCorto();
      break;
      case 'o':
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      break;
      case 'p':
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      break;
      case 'q':
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      break;
      case 'r':
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      break;
      case 's':
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      break;
      case 't':
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      break;
      case 'u':
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      break;
      case 'v':
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleCorto();
      segnaleCorto();
      segnaleCorto();
      break;
      case 'w':
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      break;
      case 'x':
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      break;
      case 'y':
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      break;
      case 'z':
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      break;
      case '?':
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      break;
      case '!':
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      break;
      case ' ':
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      break;
      case '.':
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleCorto();
      break;
      case ';':
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleLungo();
      break;
      case ',':
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      segnaleCorto();
      break;
      case '-':
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      break;
      case ':':
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      break;
      case '\'':
      segnaleCorto();
      segnaleLungo();
      segnaleCorto();
      segnaleCorto();
      segnaleLungo();
      segnaleLungo();
      break;
      default:
      break;
  }
}

void segnaleLungo(){
  digitalWrite(pin_accensione_laser, HIGH);
  delay(time_segnale_lungo);
  digitalWrite(pin_accensione_laser, LOW);
  delay(time_pausa_tra_segnali);
}

void segnaleCorto(){
  digitalWrite(pin_accensione_laser, HIGH);
  delay(time_segnale_corto);
  digitalWrite(pin_accensione_laser, LOW);
  delay(time_pausa_tra_segnali);
}
