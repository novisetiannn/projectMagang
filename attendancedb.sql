PGDMP                      |         
   attendance    15.8    16.4                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16765 
   attendance    DATABASE     �   CREATE DATABASE attendance WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Indonesia.1252';
    DROP DATABASE attendance;
                postgres    false            �            1259    16805    absensi    TABLE     �   CREATE TABLE public.absensi (
    id integer NOT NULL,
    id_karyawan integer,
    check_in timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    photo text,
    nama character varying(255)
);
    DROP TABLE public.absensi;
       public         heap    postgres    false            �            1259    16804    absensi_id_seq    SEQUENCE     �   CREATE SEQUENCE public.absensi_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.absensi_id_seq;
       public          postgres    false    219                       0    0    absensi_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.absensi_id_seq OWNED BY public.absensi.id;
          public          postgres    false    218            �            1259    16788    employee    TABLE     �   CREATE TABLE public.employee (
    id_karyawan integer NOT NULL,
    name character varying(255) NOT NULL,
    face_encoding bytea,
    photo text[],
    tgl_create timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.employee;
       public         heap    postgres    false            �            1259    16787    employee_id_karyawan_seq    SEQUENCE     �   CREATE SEQUENCE public.employee_id_karyawan_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.employee_id_karyawan_seq;
       public          postgres    false    217                       0    0    employee_id_karyawan_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.employee_id_karyawan_seq OWNED BY public.employee.id_karyawan;
          public          postgres    false    216            �            1259    16767    users    TABLE     B  CREATE TABLE public.users (
    id integer NOT NULL,
    nama character varying NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(255) NOT NULL,
    role character varying(20) NOT NULL,
    CONSTRAINT role_check CHECK (((role)::text = ANY ((ARRAY['super_admin'::character varying, 'admin'::character varying, 'karyawan'::character varying])::text[]))),
    CONSTRAINT users_role_check CHECK (((role)::text = ANY (ARRAY[('super_admin'::character varying)::text, ('admin'::character varying)::text, ('karyawan'::character varying)::text])))
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    16766    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    215                       0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    214            r           2604    16808 
   absensi id    DEFAULT     h   ALTER TABLE ONLY public.absensi ALTER COLUMN id SET DEFAULT nextval('public.absensi_id_seq'::regclass);
 9   ALTER TABLE public.absensi ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    218    219            p           2604    16791    employee id_karyawan    DEFAULT     |   ALTER TABLE ONLY public.employee ALTER COLUMN id_karyawan SET DEFAULT nextval('public.employee_id_karyawan_seq'::regclass);
 C   ALTER TABLE public.employee ALTER COLUMN id_karyawan DROP DEFAULT;
       public          postgres    false    217    216    217            o           2604    16770    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    214    215    215                      0    16805    absensi 
   TABLE DATA           I   COPY public.absensi (id, id_karyawan, check_in, photo, nama) FROM stdin;
    public          postgres    false    219   �                 0    16788    employee 
   TABLE DATA           W   COPY public.employee (id_karyawan, name, face_encoding, photo, tgl_create) FROM stdin;
    public          postgres    false    217   $!                 0    16767    users 
   TABLE DATA           C   COPY public.users (id, nama, username, password, role) FROM stdin;
    public          postgres    false    215   V5                  0    0    absensi_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.absensi_id_seq', 308, true);
          public          postgres    false    218                       0    0    employee_id_karyawan_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.employee_id_karyawan_seq', 6, true);
          public          postgres    false    216                       0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 13, true);
          public          postgres    false    214            }           2606    16813    absensi absensi_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.absensi
    ADD CONSTRAINT absensi_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.absensi DROP CONSTRAINT absensi_pkey;
       public            postgres    false    219            {           2606    16798    employee employee_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (id_karyawan);
 @   ALTER TABLE ONLY public.employee DROP CONSTRAINT employee_pkey;
       public            postgres    false    217            w           2606    16775    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    215            y           2606    16825    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public            postgres    false    215            ~           2606    16814     absensi absensi_id_karyawan_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.absensi
    ADD CONSTRAINT absensi_id_karyawan_fkey FOREIGN KEY (id_karyawan) REFERENCES public.employee(id_karyawan) ON DELETE CASCADE;
 J   ALTER TABLE ONLY public.absensi DROP CONSTRAINT absensi_id_karyawan_fkey;
       public          postgres    false    219    3195    217               c  x���M�1�םS��S.���iX"�&�	Hs{�)�vX�"�W����U���0�@@��@yDn�4�$�$2����i�|{��_��ݴ?>N��v�y�ڦo?�����R�S���%BD�%RG��Z�L#֎h��%�"�Ƙ6��-%3�R��_v������n{�1������k��ڽ�"M4�b��yU�2�l��k�E|Ř�1��I�K)c���o�2�Řzä�c�j�A{�D��A��O@��Ӈ��^SѢ�l����X"2E1n��ێ	ͧ ��i���]cʤ��^�>�ŅZ�|�iU^kw����H�S`]�Q��NZA%f������Ҙ�0��g_����=��ct-��������]j�i��Q�sb`�	0	z�w�� !��#"L���lDhX�g+��q1���(�tʉr%	�?�	�W&ù:���q�|:��F��yU���
�X-�����Q��]�4$��ӝvQ�և�f�ߓ ��.�^�A;b>��*֪b�6���$g�|D��#zv����d>�5B�7�� 	�I@��"�5�|�4%�@g<�Dtb��j2ǍJ�X����gM@ㇴ�l� ��s�            x��[ˮ]�q�~��u��ǝ�� �P QU�m�p$��A�=�/E�:�����H���Q]����ӛ��/����~/���Û�����:,�@����^��ϴ�i���ZM��zi�Ş���,����M|�{�S��e��_ߨ>����v+<�}�(��w�%��g��wx��קm��:b�<��V?ϒZ��5�x����a���?9��C����z[� 	� ��0D�=�0�:r�/���#���j�G���!4�§�;HYE�~~?ٶ���=tk��<��c4͟��}L��!ƾ���ҧ�-h����R�3�x��9��s��F���U�?=���ݱ�/;".��j��e��w��߂��!9�����O*M���g���yM~>����i�A���Y�ϯ�0��3��|~�]���ŁAu�|��B�s��*���]j��N�t�<q�Ŷ_��&�>�V���JM��'�D�k�^�~Zh��.�������-���H.��k����Ԅ�ݥI��[�f��=���o�C�>�]���|G�>���||XR33֧i�?H޲\>��C|���Y����B���|��h���a����2DF�^��݂�Uu�x�[7��� ���Fs���ē�������Wm����I+�~��c%�K���1�p�����_���*~�o��Ȟ&�y�}k�j��_�o*��(�������ya�ݟ�>kΣ��K>�X3���yĹ��+� �-�	~+J����{�F����ㅬ��������AYz��RU���V�D?/EL���I!��UH_.��uN�����v$�Uo��K�Ǆ��V���߹B��R���,��Tɿ�m��VW��`����oH&�K��go����
�-��i=��{C�����?asd����g�R=��|��J��G:��3�GL����������A���W$��W$����.>������?~��ǟ��a��?���o��M����������K��)_���ۛ���?��o_ڗ!�ޖ�Ƌ��1��4�0V(�]��dQ;�昮QS�T�����G��@�n!#J6�8�cd�k��A��e�p�T�<Z\7h�- �E�M�p_<=���B�xaB(�٭lM��y�FM#yك�eX$y�!=-���"�q�#����\c��e��Dğ��,�g6�yH)rD���P?_E���^��Ϗ�����:��T�{$�G��x}c�~KZ��X�"���8"_F�^mҗ}��pb_n��v��p��b��lD`:�y�A�Q�ˤx�bA ��G��*�U	i�:9O�u���Ȟw�[��Q��|������|ӾA������~�o����;"�+M�dOv�G��W����)���3b;|�J>��xA^�a�y��׏1V��@_/:�7�����FG�;ę�#"�+��ہ�������[>��U_/����?'�
��9�}ٵ������B<��l��H��)g�����3��5*1ܶ5=O���*T�L`t^1��9���4�?�e�����Ϡx�)�����V���{�����#�
��{_1үKg=>A���˯ $�H�+ƫ�?��a�^z>01ۧ;�Cp��w���*�d��R��?���̰7F��֊��}�_Իހ̀�~���΀���x�K�/!>�2[�O��o~���{y�o������K~������ �K �-�C=� �g�:ԗ ��"F�禑��B�5��M��o�s9T��h��̔e]���a��tx�4&0,�<��͠(�8��k�Y�>\�H)�� UDQ�����?5%5�'>=�҈Gۢ�O��t��SX���<p^�GmT����P�q�a���
H)L^gr��?8�ZM �uo���+��m�(y)���
�P�v�vS�0�h)w^�c
0|��~10���)`� w�(;�JP|�~�$t�;6r�����GG 0�;�ǫ ��j��^����D�:�R��Gh�s���� 2%�Ā� a2�7|~�Le��W��L��`�� ��c��G�����X��_���d����`�:)e���E�w�謔һp%��$�A@�P��	���ͼ<�TᏇϷ��y���lP
����H��&Dx��JA�9�����\��f� � ��"rBp"B�qw!���_}�LD�7����� p/ܛd?����ς�E����֏�*��ֈc�y���$	�2&�9⼉ ��R�a��7`j��R�19EU��F)[D���c�q��ݔ��_��J�5�:'��A��V�O���y݅�'�����hڕSΥ.݌�տ��B������G��I��6�_R}.�h<կ��_ �n�HΉo�N��D��"w�A)�����$�9��R��K*3��c����{�F.o�#\E���r[I��rlٓ�
"�e��!	�g{� �;����D� �P��k�l�bUʡ4 >wI����$9$�9͖�Br��q��R2a�oq��AGc�oΉ�a��.���n̞�2: 0�&8�@�_5�����"���+�OY��"���9��1����s��@R�3 É��/w�hT�S��=D�QHq�UM�c�(�_�ps��U��J��\�pά�Z2p�\��0C P�T����Sx������f}�< Q���@xԿ_��Q@��IJUIhs����2/�G)��*K�\�Ax;G�(��X�������b<��w�B����sjAR#H��Q�}`��!�gN�,!�<"�_�MPs�sU����Q��ܢ�ryA�z"��͚*���K�j�O>��s%��׳/�%��Z:J��4�&�,G^_y���RUt$X�Go iO`��(�~.���{��0 �$�GT#u�f�b��i�R���8(�Խ�"���]S��%�}p�z����k,e�^���%%�'���$���vD�y`Haʖ�A_K~��vn�'`��v-}	$��se���Af9��%��<��rO�+2�� �Q�����$�j[�R�+	v��DwR��w.N6a�1� �Qd��"hrbK�'r	Ff��?�FH�Μ��9���&���j��BH�F�ӌ�Ok/�D��"M�Hi2Y�B�وM�S��#�[�t<ߥ����NT%2��Ff�qP��upuv&y��U�u3B�#%�~��5
e��Ž4�j���5G��|����TZB�\�ޛy뼞X&'����W3o���� ������'�@��y�4��F�ɶ8Y�ϭ��x ��?rլk��_�O����<Ȍ�5��}�gc�domނ.!��ͥd\�s�}���P5�Vsu�Q5��VS(�!r#�Ϸ[��L�C�A��\������������=��a��������W
9z�]����͠�G����c�K�L�?i�0��An;��t�M��.Dn:�u��_��q�9*�G����/p���1޵S���$�u#5%�.�����M)'`5_/�_�T��3�̸r�&B�)H�&�?nI��vhv�����+��K�Һ�:"��_�0�zܭ�AH��F!�ĝ��7t�g�\�F����1	�;�~�I��ZwK�.�.�|j0������dk_30��2�,|=+#�3��'+A��P���x��\�^o�)l���`F�K�e�W��|����Z�o�+�+�<{�m*�~`�]j�̼�!|��=���1;�1�)���ٍ�6���m�<	�É������}2����������Mo.�@�#�+��o߅��Kb${(��Q���ʒD��r{�h���'<x_>����p���d�8���d���`kOJ���5���L�V{��1��,��� .�$��!0N�'�t�������?6"�*��2)��(SyĎrq����q0�N7|�]p�OW@�#��cz辺�E��jΔ�B��6��Rw[�F��Unm�2i}�I�@{ߣ�!T<)U����<0e���;k   f�P
g��.���nC����V\�]��>h��-3_K9O���^n7A����0W�lO�7'�����c��/XN����Ι�?vZ��ۆ��x�����w<��Kha~{9Keb,E��FN������'����2<�A�H��S��+|�d�J�_���B��)������i���=��L��$�y���)�~P�l�+�k?��ؽo � }��,�����b#��*�_�GQ�~�W
$áR&?�M�G�w!~�\��cV�LѽP$�Mv#�R3��^Oʴv�Q�@=	p���
el\��_��޵0�k-ƣ��4)߱o3��۹�7�R&U�ԕ�l�N��b]�}�ۚ-�<��ޟ���R�3����}Ea�D�ݓn�ɽ�39J��!�)�Q�E�p����,�l{rI�[�����@������[[�����{Sb�Y�s(��[��^B�Q�eA�"�k�9%f��2�V�K�295&�ҴF���B�RV	!}�-1����8�[�d����f�C(K1*�0�߳h�[`�j�:�����A#yh8���a���mQW�?BA:�Li��g{�P}��p����F�Hs�To�	�#��2tG�fQ�r�nj�pJWk�P|��!k{4�z���,���!����>�(6��k�g������T��t�����B��C�򔱌[6s�|g�r(�u��ؒw��q������=�X�Q�ّo�~��󗘛=�y��ȟlI�o�6�k�z����;�0�6�SWd�l[�zK���]�Qf��7��8�4��[,�Hͳ�NP���n��Qe�̵��ނl�Z�*[)k���A��&+q�8��(�V�ߣ�ۯr���2��ݸ��/;�"|�G�^���O���7����?�,�t�4j�:�e�{1�h� �$	W�B���H6�~?��BTzч�k|k�X�ů6�����)����/S
P0�g��B}p����3� �*��9M}}����t-M�o!�e��-��� ��>�j�X��6�m��u�~���	|�oCz�K�/5>�۞�{~zz�_����         p  x���[O�@ǟ˧��r�>c����"+n61s�m��
|����&��p2gfr��s��/����ѨxJ��ˁ~��/�2���m�E1�ˢ���# �e���&�y�Ԏ�U<l���t����,��j7~��8��v��5�u�,� �A��U�%� ��&l�g�D��N��E|���N&����<_���(���M��s;�T�u����DKF/zGc_�:O��q^/>Ȯ��|��k��	���aR�~2)����:h�0�0R�S
�1�{0�c��Y##��� $���7 %�:һ�K��Y�X����7��G{̰К1�!�hm0�SZ`�)u��@:&e a4��� YCA� 5�Hځ�A:�-��f�P:��/��qn�W�i�4�6L�6�Y�(��s�0�J$<5�QK<}AQ��K}������v~t11ygս�c&y�"i �N�j�B��)���\E�tB�o#0�h�hS.%�yp�(���|���L�����wzs*�i
���J�Q�n5�:�HSBN-� $�!8��{'!ͤ���`��'�P�n�k���zz��{3���]1��}�{w�=�W�i�_���*ݞd3uS�7ſǭV��PFY     