ob1 = imread('object1.png') > 0;
ob2 = imread('object2.png') > 0;
ob2t = imread('object2t.png') > 0;
ob3 = imread('object3.png') > 0;                                        

T1 = align_shape(ob2, ob2t);
T2 = align_shape(ob2, ob1);
T3 = align_shape(ob2, ob3);