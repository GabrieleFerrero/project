public class Principale extends PrincipaleProcessing{
    public static final float INCREMENTO_MOTORI = 0.5F;
    private int raggio_circonferenza = 50;
    private Arduino arduino;
    private float[] motori_precedenti = new float[]{0,0,0,0,58};
    private Tabella tbl = new Tabella(this, 300, 400, 6, 2,
            20, 18);
    private boolean eInizializzata = false;
    private int e20 = 0;


    public static void main(String[] args){
        Principale pc = new Principale();

        LeapProcessing lp = new LeapProcessing("Principale");

    }

    @Override
    public void addPAappletComponents() {
        if(!eInizializzata){
            //comunicazioneArduino = new ComunicazioneArduino();
            //comunicazioneArduino.initialize();
            this.inizializzaArduino();
            eInizializzata = true;
        }

        //getHands()[0] is the right hand, getHands()[1] is the left hand.
        //text(super.getHands()[0].getDataHand().getCoordPalmoProcessing()[0]+"", 200, 200);
        this.disegnaJoyStick( (float)(width-300)/4, 300, true);
        this.disegnaJoyStick( (float)(width-300)*3/4, 300, false);
        this.tbl.drawTabella();
        this.completaTabella();
        if(e20 != 20){
            e20++;
        }
        else {
            e20 = 0;
            this.inviaDatiArduino();
        }

    }

    public void disegnaJoyStick(float centro_x, float width_tabella, boolean isJoyStickSinistra){
        strokeWeight(2);
        stroke(24,159,151);
        fill(24,159,151);
        //float centro_x = (width-width_tabella)/4;

        rect(centro_x-(width-width_tabella)/8, (float) ((height*3/5)-50),
                (width-width_tabella)/4, 100);
        if(isJoyStickSinistra){
            rect(centro_x-50, (float) (height*3/5)-(float)height/8,
                    100, (float)(height/4));
       }
        fill(244,159,151);
        ellipse(centro_x, (float) (height*3/5), this.raggio_circonferenza*2, this.raggio_circonferenza*2);
    }


    public void completaTabella(){
        this.tbl.pushTestoInTabella("Motore", 0, 0, new int[]{7, 59, 76});
        this.tbl.pushTestoInTabella("Valore\nin gradi", 1, 0, new int[]{7, 59, 76});

        this.tbl.pushTestoInTabella("distanza indice\npollice", 0, 1, new int[]{7, 59, 76});
        this.tbl.pushTestoInTabella(String.valueOf(this.getHands()[0].thumbIndexDistance()),
                1, 1,new int[]{7, 59, 76});

        this.motori_precedenti[4] = this.getHands()[0].thumbIndexDistance();
        if(this.motori_precedenti[4] < 58){
            this.motori_precedenti[4] = 58;
        }
        else if(motori_precedenti[4] > 108){
            this.motori_precedenti[4] = 108;
        }

        for(int a = 0; a < 4; a++){
            //Mano destra: destra-sinistra muove il motore 3, distanza pollice e indice muove il motore 4
            //Mano sinistra: destra-sinistra muove il motore 0, avanti-indietro muove il motore 1-2
            this.tbl.pushTestoInTabella("direzione motore "+a+" :", 0, a+2, new int[]{7, 59, 76});
            String testo = switch (a) {
                case 0 -> posizioneMano((float) (width - 300) / 4, (float) (height * 3 / 5),
                        this.getHands()[1].getDataHand().getCoordPalmProcessing()[0],
                        this.getHands()[1].getDataHand().getCoordPalmProcessing()[1], 0);
                case 1, 2 -> this.invertiFrecce(posizioneMano((float) (height * 3 / 5), (float) (width - 300) / 4,
                        this.getHands()[1].getDataHand().getCoordPalmProcessing()[1],
                        this.getHands()[1].getDataHand().getCoordPalmProcessing()[0], a), a);
                case 3 -> posizioneMano((float) (width - 300) * 3 / 4, (float) (height * 3 / 5),
                        this.getHands()[0].getDataHand().getCoordPalmProcessing()[0],
                        this.getHands()[0].getDataHand().getCoordPalmProcessing()[1], 3);
                default -> "";
            };
            this.tbl.pushTestoInTabella(testo, 1, a+2, new int[]{7, 59, 76});
        }
    }

    public String invertiFrecce(String testo, int n_motore){
        if(testo.equals("->")){
            testo = "<-";
            this.motori_precedenti[n_motore] = Math.max(this.motori_precedenti[n_motore]-INCREMENTO_MOTORI*2, 0);
        }
        else if(testo.equals("<-")){
            testo = "->";
            this.motori_precedenti[n_motore] = Math.min(this.motori_precedenti[n_motore]+INCREMENTO_MOTORI*2, 180);
        }
        return testo;
    }

    public String posizioneMano(float centro_x, float centro_y, float coord_x, float coord_y, int n_motore){
        String testo = "==";
        if(calcolaDistanzaPunti(new float[]{centro_x, centro_y}, new float[]{coord_x, coord_y}) <=
                this.raggio_circonferenza){
            testo = "==";
        }
        else if(coord_x > (float)(centro_x+this.raggio_circonferenza) ||
                coord_x < (float)(centro_x-this.raggio_circonferenza)){
            if(centro_x < coord_x){
                testo="->";
                this.motori_precedenti[n_motore] = Math.min(this.motori_precedenti[n_motore]+INCREMENTO_MOTORI, 180);
            }
            else{
                testo = "<-";
                this.motori_precedenti[n_motore] = Math.max(this.motori_precedenti[n_motore]-INCREMENTO_MOTORI, 0);
            }
        }
        return  testo;
    }

    public float calcolaDistanzaPunti(float[] coord_nodo1, float[] coord_nodo2){

        float result_x = (float) Math.pow(coord_nodo1[0]-coord_nodo2[0],2);
        float result_y = (float) Math.pow(coord_nodo1[1]-coord_nodo2[1],2);
        float somma_coord = result_x + result_y;

        return (float) Math.sqrt(somma_coord);
    }

    public void inviaDatiArduino(){
        for(int a = 0; a < motori_precedenti.length; a++){
            System.out.println(a+":"+(int)this.motori_precedenti[a]+"#");
            arduino.serialWrite(a+":"+(int)this.motori_precedenti[a]+"#");
        }


    }
    public void inizializzaArduino(){
        String ArduinoPort = "/dev/ttyACM0"; //Your port name here
        int BAUD_RATE = 230400;
        this.arduino = new Arduino(ArduinoPort, BAUD_RATE);
        this.arduino.openConnection();
        this.inviaDatiArduino();
    }



}