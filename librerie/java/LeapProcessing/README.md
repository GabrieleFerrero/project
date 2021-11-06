# LeapProcessing library

With this library we are going to manage the inputs that the [LeapMotion](https://www.ultraleap.com/product/leap-motion-controller/) gives us back by going to draw them with processing.

## Examples

![es1](es1.gif)

## Tutorial

1. Install the LeapMotion SDK, choosing the OS you are using.

2. After extracting the file, install the .deb / .exe / .dmg program present in the downloaded folder

3. Create an IntelliJ idea project, following the steps in the video below

#### This is the code used in the video

```java
public class Principale extends PrincipaleProcessing{

    public static void main(String[] args){
        LeapProcessing lp = new LeapProcessing("Principale");

    }

    @Override
    public void addPAappletComponents() {
        //getHands()[0] is the right hand, getHands()[1] is the left hand.
        text(super.getHands()[0].getDataHand().getCoordPalmoProcessing()[0]+"", 200, 200);
    }
}
```

## Libraries used

- [Leap Motion](https://developer-archive.leapmotion.com/documentation/java/devguide/Leap_SDK_Overview.html)
- [Processing](https://processing.org/)

## Authors

- [@IsabellaBianco](https://github.com/IsabellaBianco)
- [@GabrieleFerrero](https://github.com/GabrieleFerrero)

  
