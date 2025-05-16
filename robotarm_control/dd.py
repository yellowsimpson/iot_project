


int servoParallelControl (int thePoos, Servo, theServo, int speed){
    int starPos = theServo.read();
    int newPos = starPos;
}

if (startPos < (thePos)){
    newPos = newPos + 1;
    theServo.write(newPos);
    delay(speed);
    return 0;
}

else if (newPos > (thePos)){
    newPose =newPos - 1;
    theServo.write(newPos);
    delay(speed);
    return 0;
}

else{
    return 1;
}
}