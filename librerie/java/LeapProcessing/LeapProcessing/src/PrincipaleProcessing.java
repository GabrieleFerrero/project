import processing.core.PApplet;

public abstract class PrincipaleProcessing extends PApplet{
    private Mano[] mani = new Mano[2];
    private ClientUDP ck;

    public void settings() {
        size(displayWidth, displayHeight, P3D);
    }
    public void setup() {

        for(int a = 0; a < mani.length; a++){
            mani[a] = new Mano(this, displayWidth, displayHeight, 10);
        }
        try {
            ck = new ClientUDP("PrincipaleProcessing");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

    }

    public void draw() {
        background(222, 243, 216);
        try {
            this.analizzaMessaggioRicevuto();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        this.addPAappletComponents();

    }

    public void analizzaMessaggioRicevuto() throws Exception {
        String[] messaggio = this.ck.riceviMessaggio().split("°");
        if(messaggio[0].equals("LeapListener")){
            this.disegnaMani(messaggio[1]);
        }
    }

    public void disegnaMani(String messaggio_ricevuto){
        try {
            for (Mano mano : mani) {
                mano.getDataHand().inizializzaCoordinate();
            }
            if(!messaggio_ricevuto.equals("_")){
                    String[] messaggio = messaggio_ricevuto.split("_");


                if (messaggio[0].equals("DX")) {
                    mani[0].getDataHand().setDataMano(messaggio[1]);
                }
                if (messaggio[0].equals("SX")) {
                    mani[1].getDataHand().setDataMano(messaggio[1]);
                }
                if (messaggio.length >= 3 && messaggio[2] != null) {
                    System.out.println("messaggio 2: " + messaggio[2]);
                    if (messaggio[2].equals("DX")) {
                        mani[0].getDataHand().setDataMano(messaggio[3]);
                    }
                    if (messaggio[2].equals("SX")) {
                        mani[1].getDataHand().setDataMano(messaggio[3]);
                    }
                }

            }
        } catch (Exception e) {
            System.out.println("Eccezione: "+e.getMessage());
        }
        for (Mano mano : mani) {
            mano.aggiornaMano();
        }

    }

    public Mano[] getHands() {
        //getHands()[0] is the right hand, getHands()[1] is the left hand.
        return mani;
    }

    public abstract void addPAappletComponents();

}
