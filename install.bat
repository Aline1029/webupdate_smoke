@echo off
color a
:loop
echo.
echo ************************************************************
echo *                                                          *
echo *                                                         	*
echo *     ����4.1��ϴǮϵͳBS                                	    *
echo *                                                          *
echo *                                                          *
echo ************************************************************
echo.
title ������ϴǮϵͳ����
set /p tnsname=���������ݿ������
set /p hsconuser=�������û���:
set /p hsconpwd=���������룺

:choose
echo.
echo ************************************************************
echo *                                                          *
echo * ��ѡ��������ϵͳ����ҵ:                        		        *
echo *     1��BS����                     			            *
echo *     2��BS���� 				                            *
echo *     3��CS����					                            *
echo *     4��CS����					                            *
echo *     C���˳���װ                                          	*
echo *                                                          *
echo ************************************************************
echo.
set /p dropbackflag=�������"C"���˳���������:
if %dropbackflag%==C goto end
if %dropbackflag%==c goto end
if %dropbackflag%==1 goto installbsjj
if %dropbackflag%==2 goto installbsxt
if %dropbackflag%==3 goto installcsjs
if %dropbackflag%==4 goto installcsxt
goto end


:installbsjj
echo.
echo ************************************************************
echo *                                                          *
echo *                                                          *
echo *             ��������:BS����                    *
echo *                                                          *
echo *                                                          *
echo ************************************************************
sqlplus %hsconuser%/%hsconpwd%@%tnsname% @.\Installbsjj.sql 
type .\log\install.log | find /i /n "ora-" > .\log\install.txt
type .\log\install.log | find /i /n "����" >> .\log\install.txt
type .\log\install.log | find /i /n "SP2" >> .\log\install.txt
echo.
type .\log\install.txt
find /v "" /c  .\log\install.txt

:installbsxt
echo.
echo ************************************************************
echo *                                                          *
echo *                                                          *
echo *             ��������:BS����                    *
echo *                                                          *
echo *                                                          *
echo ************************************************************
sqlplus %hsconuser%/%hsconpwd%@%tnsname% @.\Installbsxt.sql 
type .\log\install.log | find /i /n "ora-" > .\log\install.txt
type .\log\install.log | find /i /n "����" >> .\log\install.txt
type .\log\install.log | find /i /n "SP2" >> .\log\install.txt
echo.
type .\log\install.txt
find /v "" /c  .\log\install.txt

if %errorlevel% == 0 (
echo.
echo ************************************************************
echo *                                                                                     	*
echo *        ������ϣ������ִ�����鿴���������Ϣ          	*
echo *                                                                                    	*
echo ************************************************************
echo.
goto end
) else (
echo.
echo ************************************************************
echo *                                                          	*
echo *                         �����ɹ�                    	*
echo *                                                          	*
echo ************************************************************
echo.
goto finsh
)
:finsh
echo.
echo ************************************************************
echo *                                                           	*
echo *                                                           	*
echo *             ������ϴǮ4.1�����������    	*
echo *                                                           	*
echo *                                                           	*
echo ************************************************************
echo.
goto end
:end
echo ��������˳�
pause > nul

