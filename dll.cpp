// sampleDLL.java 
import java.util.Scanner; 
public class sampleDLL 
{ 
static 
{ 
System.loadLibrary("sampleDLL"); 
} public static void main(String 
args[]) 
{ 
Scanner scanner = new Scanner(System.in); 
int num1 = 0, num2 = 0; 
System.out.println("DLL Addition Operation"); 
System.out.print("Enter first number: "); num1 
= scanner.nextInt(); 
System.out.print("Enter second number: "); 
num2 = scanner.nextInt(); 
System.out.println("ADDITION IS: "+new sampleDLL().add(num1,num2)); 
System.out.println("SUBSTACTION IS: "+new 
sampleDLL().sub(num1,num2)); 
System.out.println("Multiplication IS: "+new sampleDLL().mul(num1,num2)); 
} public native int add(int num1, int 
num2); public native int sub(int num1, int 
num2); public native int mul(int num1, 
int num2); 
} 
//sampleDLL.c 
#include<jni.h> 
#include<stdio.h> 
#include "sampleDLL.h" 
JNIEXPORT jint JNICALL Java_sampleDLL_add 
(JNIEnv *env, jobject thisobj, jint num1, jint num2) 
{ return 
num1+num2; } 
JNIEXPORT jint JNICALL Java_sampleDLL_sub 
(JNIEnv *env, jobject thisobj, jint num1, jint num2) 
{ return num1
num2; 
} 
JNIEXPORT jint JNICALL Java_sampleDLL_mul 
(JNIEnv *env, jobject thisobj, jint num1, jint num2) 
{ return 
num1*num2; } 



//command

/*
javac -h . testJni2.java
 gcc -c -fPIC -I/usr/lib/jvm/java-1.11.0-openjdk-amd64/include -I/usr/lib/jvm/java-1.11.0-openjdk-amd64/inc
lude/linux testJni2.c -o testJni2.o
 gcc -shared -fPIC -o libnative.so testJnt2.o -lc
 java -Djava. ltbrary.path =. testJnt2
 */