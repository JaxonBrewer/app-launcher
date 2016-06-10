FasdUAS 1.101.10   ��   ��    k             l      ��  ��   
	This script is automatically generated. It's used to wrap applications that behave poorly.
	Some applications like to force updates or require world read/write permissions, which we
	don't generally like in our sort of environment. This allows us to keep everything locked
	up carefully.
	
	COPYRIGHT (c) 2015 Marriott Library IT Services.  All rights reserved.
	Author:			Pierce Darragh - pierce.darragh@utah.edu
	Creation Date:	May 7, 2015
	Last Updated:		May 12, 2015
	Permission to use, copy, modify, and distribute this software and its documentation for any
	purpose and without fee is hereby granted, provided that the above copyright notice appears in
	all copies and that both that copyright notice and this permission notice appear in supporting
	documentation, and that the name of The Marriott Library not be used in advertising or
	publicity pertaining to distribution of the software without specific, written prior permission.
	This software is supplied as-is without expressed or implied warranties of any kind.
     � 	 	 
 	 T h i s   s c r i p t   i s   a u t o m a t i c a l l y   g e n e r a t e d .   I t ' s   u s e d   t o   w r a p   a p p l i c a t i o n s   t h a t   b e h a v e   p o o r l y . 
 	 S o m e   a p p l i c a t i o n s   l i k e   t o   f o r c e   u p d a t e s   o r   r e q u i r e   w o r l d   r e a d / w r i t e   p e r m i s s i o n s ,   w h i c h   w e 
 	 d o n ' t   g e n e r a l l y   l i k e   i n   o u r   s o r t   o f   e n v i r o n m e n t .   T h i s   a l l o w s   u s   t o   k e e p   e v e r y t h i n g   l o c k e d 
 	 u p   c a r e f u l l y . 
 	 
 	 C O P Y R I G H T   ( c )   2 0 1 5   M a r r i o t t   L i b r a r y   I T   S e r v i c e s .     A l l   r i g h t s   r e s e r v e d . 
 	 A u t h o r : 	 	 	 P i e r c e   D a r r a g h   -   p i e r c e . d a r r a g h @ u t a h . e d u 
 	 C r e a t i o n   D a t e : 	 M a y   7 ,   2 0 1 5 
 	 L a s t   U p d a t e d : 	 	 M a y   1 2 ,   2 0 1 5 
 	 P e r m i s s i o n   t o   u s e ,   c o p y ,   m o d i f y ,   a n d   d i s t r i b u t e   t h i s   s o f t w a r e   a n d   i t s   d o c u m e n t a t i o n   f o r   a n y 
 	 p u r p o s e   a n d   w i t h o u t   f e e   i s   h e r e b y   g r a n t e d ,   p r o v i d e d   t h a t   t h e   a b o v e   c o p y r i g h t   n o t i c e   a p p e a r s   i n 
 	 a l l   c o p i e s   a n d   t h a t   b o t h   t h a t   c o p y r i g h t   n o t i c e   a n d   t h i s   p e r m i s s i o n   n o t i c e   a p p e a r   i n   s u p p o r t i n g 
 	 d o c u m e n t a t i o n ,   a n d   t h a t   t h e   n a m e   o f   T h e   M a r r i o t t   L i b r a r y   n o t   b e   u s e d   i n   a d v e r t i s i n g   o r 
 	 p u b l i c i t y   p e r t a i n i n g   t o   d i s t r i b u t i o n   o f   t h e   s o f t w a r e   w i t h o u t   s p e c i f i c ,   w r i t t e n   p r i o r   p e r m i s s i o n . 
 	 T h i s   s o f t w a r e   i s   s u p p l i e d   a s - i s   w i t h o u t   e x p r e s s e d   o r   i m p l i e d   w a r r a n t i e s   o f   a n y   k i n d . 
   
  
 p         ������ 0 mypath myPath��        p         ������ 0 appname appName��        p         ������ 0 diskname diskName��        p         ������ 0 apppath appPath��        p         ������ 0 	imagepath 	imagePath��        p         ������ 0 
shadowpath 
shadowPath��        p         ������ 0 binname binName��         p       ! ! ������ 0 	mountroot 	mountRoot��      " # " p       $ $ ������ 0 currentuser currentUser��   #  % & % p       ' ' ������ 0 reownscript reownScript��   &  ( ) ( l     ��������  ��  ��   )  * + * i      , - , I     ������
�� .aevtoappnull  �   � ****��  ��   - k     g . .  / 0 / l     �� 1 2��   1 + % Set all of the locations for things.    2 � 3 3 J   S e t   a l l   o f   t h e   l o c a t i o n s   f o r   t h i n g s . 0  4 5 4 l     �� 6 7��   6 ^ X Most likely, you'll only ever need to change the 'appName'. If you give everything else    7 � 8 8 �   M o s t   l i k e l y ,   y o u ' l l   o n l y   e v e r   n e e d   t o   c h a n g e   t h e   ' a p p N a m e ' .   I f   y o u   g i v e   e v e r y t h i n g   e l s e 5  9 : 9 l     �� ; <��   ; 2 , similar names, it'll make your life easier.    < � = = X   s i m i l a r   n a m e s ,   i t ' l l   m a k e   y o u r   l i f e   e a s i e r . :  > ? > l     ��������  ��  ��   ?  @ A @ l     �� B C��   B , & appName:		the name of the application    C � D D L   a p p N a m e : 	 	 t h e   n a m e   o f   t h e   a p p l i c a t i o n A  E F E l     �� G H��   G &   diskName:		the name of the disk    H � I I @   d i s k N a m e : 	 	 t h e   n a m e   o f   t h e   d i s k F  J K J l     �� L M��   L 9 3 appPath:		the path to the application in the image    M � N N f   a p p P a t h : 	 	 t h e   p a t h   t o   t h e   a p p l i c a t i o n   i n   t h e   i m a g e K  O P O l     �� Q R��   Q 7 1 imagePath:		the path to the image in this bundle    R � S S b   i m a g e P a t h : 	 	 t h e   p a t h   t o   t h e   i m a g e   i n   t h i s   b u n d l e P  T U T l     �� V W��   V L F shadowPath:	the path to the shadow file for when the image is mounted    W � X X �   s h a d o w P a t h : 	 t h e   p a t h   t o   t h e   s h a d o w   f i l e   f o r   w h e n   t h e   i m a g e   i s   m o u n t e d U  Y Z Y l     �� [ \��   [ M G binName:		the location of the executable binary inside the application    \ � ] ] �   b i n N a m e : 	 	 t h e   l o c a t i o n   o f   t h e   e x e c u t a b l e   b i n a r y   i n s i d e   t h e   a p p l i c a t i o n Z  ^ _ ^ l     �� ` a��   ` \ V mountRoot:	the location to mount the volume under (change for obnoxious applications)    a � b b �   m o u n t R o o t : 	 t h e   l o c a t i o n   t o   m o u n t   t h e   v o l u m e   u n d e r   ( c h a n g e   f o r   o b n o x i o u s   a p p l i c a t i o n s ) _  c d c r     	 e f e l     g���� g I    �� h i
�� .earsffdralis        afdr h  f      i �� j��
�� 
rtyp j m    ��
�� 
utxt��  ��  ��   f o      ���� 0 mypath myPath d  k l k r   
  m n m m   
  o o � p p  C a l c u l a t o r n o      ���� 0 appname appName l  q r q r     s t s o    ���� 0 appname appName t o      ���� 0 diskname diskName r  u v u r     w x w b     y z y b     { | { b     } ~ } o    ���� 0 diskname diskName ~ m       � � �  : | o    ���� 0 appname appName z m     � � � � �  . a p p x o      ���� 0 apppath appPath v  � � � r    ) � � � c    ' � � � n    % � � � 1   # %��
�� 
psxp � l   # ����� � b    # � � � b    ! � � � b     � � � o    ���� 0 mypath myPath � m     � � � � � & C o n t e n t s : R e s o u r c e s : � o     ���� 0 appname appName � m   ! " � � � � �  . d m g��  ��   � m   % &��
�� 
utxt � o      ���� 0 	imagepath 	imagePath �  � � � r   * 5 � � � b   * 1 � � � b   * / � � � n   * - � � � 1   + -��
�� 
psxp � m   * + � � � � � 
 : t m p : � o   - .���� 0 appname appName � m   / 0 � � � � �  . s h a d o w � o      ���� 0 
shadowpath 
shadowPath �  � � � r   6 E � � � n   6 A � � � 1   ? A��
�� 
psxp � l  6 ? ����� � b   6 ? � � � b   6 ; � � � o   6 7���� 0 apppath appPath � m   7 : � � � � �   : C o n t e n t s : M a c O S : � m   ; > � � � � �  n w j s��  ��   � o      ���� 0 binname binName �  � � � r   F M � � � m   F I � � � � �  / V o l u m e s � o      ���� 0 	mountroot 	mountRoot �  � � � r   N Y � � � I  N U�� ���
�� .sysoexecTEXT���     TEXT � l  N Q ����� � m   N Q � � � � �  w h o a m i��  ��  ��   � o      ���� 0 currentuser currentUser �  � � � r   Z a � � � m   Z ] � � � � � T / u s r / l o c a l / b i n / h i g h f i v e a p p _ c h a n g e _ o w n e r . s h � o      ���� 0 reownscript reownScript �  � � � l  b b��������  ��  ��   �  ��� � n  b g � � � I   c g�������� 0 main  ��  ��   �  f   b c��   +  � � � l     ��������  ��  ��   �  � � � i     � � � I      �������� 0 main  ��  ��   � k     % � �  � � � l     ��������  ��  ��   �  � � � l     �� � ���   � + % If the application is running, quit.    � � � � J   I f   t h e   a p p l i c a t i o n   i s   r u n n i n g ,   q u i t . �  � � � l     �� � ���   �   Otherwise, launch it!    � � � � ,   O t h e r w i s e ,   l a u n c h   i t ! �  ��� � Z     % � ��� � � l     ����� � I     �������� 0 	isrunning 	isRunning��  ��  ��  ��   � k     � �  � � � I   �� � �
�� .sysodlogaskr        TEXT � l    ����� � b     � � � o    	���� 0 appname appName � m   	 
 � � � � � (   i s   a l r e a d y   r u n n i n g !��  ��   � �� � �
�� 
btns � J     � �  ��� � m     � � � � � 0 T h a n k s   f o r   t h e   r e m i n d e r !��   � �� � �
�� 
dflt � m    ����  � �� � �
�� 
givu � m    ����  � �� ���
�� 
disp � m    ��
�� stic   ��   �  ��� � L    ����  ��  ��   � I   %�� ���
�� .ascrnoop****      � **** � J    !����  ��  ��   �  � � � l     ��������  ��  ��   �  � � � l     �� � ��   �    Launches the application.     � 4   L a u n c h e s   t h e   a p p l i c a t i o n . �  i     I     ����
�� .ascrnoop****      � **** J      ����  ��   k     L 	 l     �������  ��  �  	 

 l     �~�~   , & If the disk is not mounted, mount it.    � L   I f   t h e   d i s k   i s   n o t   m o u n t e d ,   m o u n t   i t .  l     �}�}   B < If after this the path to the executable exists, launch it.    � x   I f   a f t e r   t h i s   t h e   p a t h   t o   t h e   e x e c u t a b l e   e x i s t s ,   l a u n c h   i t . �| O     L k    K  Z    5�{�z H     l   �y�x I   �w�v
�w .coredoexbool        obj  4    �u
�u 
cdis o    �t�t 0 diskname diskName�v  �y  �x   k    1   !"! l   �s#$�s  # ) # Mount the image at imagePath with:   $ �%% F   M o u n t   t h e   i m a g e   a t   i m a g e P a t h   w i t h :" &'& l   �r()�r  ( U O  * -nobrowse			Prevents the volume from appearing in Finder or on the Desktop.   ) �** �     *   - n o b r o w s e 	 	 	 P r e v e n t s   t h e   v o l u m e   f r o m   a p p e a r i n g   i n   F i n d e r   o r   o n   t h e   D e s k t o p .' +,+ l   �q-.�q  - c ]  * -noautoopenro		Makes sure we won't accidentally pop open a Finder window into the volume.   . �// �     *   - n o a u t o o p e n r o 	 	 M a k e s   s u r e   w e   w o n ' t   a c c i d e n t a l l y   p o p   o p e n   a   F i n d e r   w i n d o w   i n t o   t h e   v o l u m e ., 010 l   �p23�p  2 ^ X  * -noverify				Ensures that hdiutil will not verify the volume. Speeds up mount times.   3 �44 �     *   - n o v e r i f y 	 	 	 	 E n s u r e s   t h a t   h d i u t i l   w i l l   n o t   v e r i f y   t h e   v o l u m e .   S p e e d s   u p   m o u n t   t i m e s .1 565 l   �o78�o  7 > 8  * -mountroot			Changes where the volume is mounted to.   8 �99 p     *   - m o u n t r o o t 	 	 	 C h a n g e s   w h e r e   t h e   v o l u m e   i s   m o u n t e d   t o .6 :;: l   �n<=�n  < � �  * -shadow 				Allows read/write access by creating a file the user can edit and shadowing what would have been the edits there.   = �>>     *   - s h a d o w   	 	 	 	 A l l o w s   r e a d / w r i t e   a c c e s s   b y   c r e a t i n g   a   f i l e   t h e   u s e r   c a n   e d i t   a n d   s h a d o w i n g   w h a t   w o u l d   h a v e   b e e n   t h e   e d i t s   t h e r e .; ?@? l   �m�l�k�m  �l  �k  @ ABA I   !�jC�i
�j .sysoexecTEXT���     TEXTC l   D�h�gD b    EFE b    GHG b    IJI b    KLK b    MNM m    OO �PP � h d i u t i l   a t t a c h   - n o b r o w s e   - o w n e r s   o n   - n o a u t o o p e n r o   - n o v e r i f y   - m o u n t r o o t  N o    �f�f 0 	mountroot 	mountRootL m    QQ �RR    - s h a d o w  J o    �e�e 0 
shadowpath 
shadowPathH m    SS �TT   F n    UVU 1    �d
�d 
strqV o    �c�c 0 	imagepath 	imagePath�h  �g  �i  B WXW l  " "�b�a�`�b  �a  �`  X YZY l  " "�_�^�]�_  �^  �]  Z [\[ l  " "�\�[�Z�\  �[  �Z  \ ]^] l  " "�Y�X�W�Y  �X  �W  ^ _`_ l  " "�V�U�T�V  �U  �T  ` aba l  " "�S�R�Q�S  �R  �Q  b cdc I  " /�Pe�O
�P .sysoexecTEXT���     TEXTe l  " +f�N�Mf b   " +ghg b   " )iji b   " 'klk m   " #mm �nn 
 s u d o  l l  # &o�L�Ko n   # &pqp 1   $ &�J
�J 
strqq o   # $�I�I 0 reownscript reownScript�L  �K  j m   ' (rr �ss   h o   ) *�H�H 0 currentuser currentUser�N  �M  �O  d t�Gt l  0 0�F�E�D�F  �E  �D  �G  �{  �z   uvu l  6 6�C�B�A�C  �B  �A  v wxw l  6 6�@yz�@  y ' ! Launch the app for the user too.   z �{{ B   L a u n c h   t h e   a p p   f o r   t h e   u s e r   t o o .x |�?| Z   6 K}~�>�=} I  6 =�<�;
�< .coredoexbool        obj  o   6 9�:�: 0 apppath appPath�;  ~ I  @ G�9��8
�9 .aevtodocnull  �    alis� o   @ C�7�7 0 apppath appPath�8  �>  �=  �?   m     ���                                                                                  MACS  alis    h  Mac OS X                   �ۘ=H+   F0'
Finder.app                                                      HԞ���        ����  	                CoreServices    ���      ��o�     F0' F0& F0%  2Mac OS X:System: Library: CoreServices: Finder.app   
 F i n d e r . a p p    M a c   O S   X  &System/Library/CoreServices/Finder.app  / ��  �|   ��� l     �6�5�4�6  �5  �4  � ��� l     �3���3  � ] W Returns a boolean telling whether the application is currently running from the image.   � ��� �   R e t u r n s   a   b o o l e a n   t e l l i n g   w h e t h e r   t h e   a p p l i c a t i o n   i s   c u r r e n t l y   r u n n i n g   f r o m   t h e   i m a g e .� ��� i    ��� I      �2�1�0�2 0 	isrunning 	isRunning�1  �0  � Q     ���� k    �� ��� r    ��� l   ��/�.� I   �-��,
�- .sysoexecTEXT���     TEXT� b    ��� b    ��� m    �� ���  p g r e p   - f   '� o    �+�+ 0 binpath binPath� m    �� ���  '�,  �/  �.  � o      �*�* 0 	psresults 	psResults� ��)� L    �� m    �(
�( boovtrue�)  � R      �'�&�%
�' .ascrerr ****      � ****�&  �%  � L    �� m    �$
�$ boovfals� ��#� l     �"�!� �"  �!  �   �#       �������  � ����
� .aevtoappnull  �   � ****� 0 main  
� .ascrnoop****      � ****� 0 	isrunning 	isRunning� � -�����
� .aevtoappnull  �   � ****�  �  �  � ���� o��  �� � ��� � �� � �� �� ��
�	 ���
� 
rtyp
� 
utxt
� .earsffdralis        afdr� 0 mypath myPath� 0 appname appName� 0 diskname diskName� 0 apppath appPath
� 
psxp� 0 	imagepath 	imagePath� 0 
shadowpath 
shadowPath� 0 binname binName� 0 	mountroot 	mountRoot
�
 .sysoexecTEXT���     TEXT�	 0 currentuser currentUser� 0 reownscript reownScript� 0 main  � h)��l E�O�E�O�E�O��%�%�%E�O��%�%�%�,�&E�O��,�%�%E` O�a %a %�,E` Oa E` Oa j E` Oa E` O)j+ � � ������� 0 main  �  �  �  � �� ��  ������������������ 0 	isrunning 	isRunning� 0 appname appName
�  
btns
�� 
dflt
�� 
givu�� 
�� 
disp
�� stic   �� 
�� .sysodlogaskr        TEXT
�� .ascrnoop****      � ****� &*j+   ��%��kv�k����� OhY jvj � ����������
�� .ascrnoop****      � ****��  ��  �  � �������O��Q��S������m��r������
�� 
cdis�� 0 diskname diskName
�� .coredoexbool        obj �� 0 	mountroot 	mountRoot�� 0 
shadowpath 
shadowPath�� 0 	imagepath 	imagePath
�� 
strq
�� .sysoexecTEXT���     TEXT�� 0 reownscript reownScript�� 0 currentuser currentUser�� 0 apppath appPath
�� .aevtodocnull  �    alis�� M� I*��/j  &��%�%�%�%��,%j O���,%�%�%j OPY hO_ j  _ j Y hU� ������������� 0 	isrunning 	isRunning��  ��  � ������ 0 binpath binPath�� 0 	psresults 	psResults� ��������
�� .sysoexecTEXT���     TEXT��  ��  ��  �%�%j E�OeW 	X  fascr  ��ޭ