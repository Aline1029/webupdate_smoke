@echo off
color a
:loop
echo.
echo ************************************************************
echo *                                                          *
echo *                                                         	*
echo *     恒生4.1反洗钱系统BS                                	    *
echo *                                                          *
echo *                                                          *
echo ************************************************************
echo.
title 恒生4.1反洗钱系统升级
    set tnsname="BS38.95"
set hsconuser="bsaml"
set hsconpwd="bsaml"
:choose
echo.
echo ************************************************************
echo *                                                          *
echo * 请选择升级的系统和行业:                        		        *
echo *     1－BS基金                     			            *
echo *     2－BS信托 				                            *
echo *     3－CS基金					                            *
echo *     4－CS信托					                            *											
echo *     C－退出安装                                          	*
echo *                                                          *
echo ************************************************************
echo.
set /p dropbackflag=如果输入"C"将退出升级过程:
if %dropbackflag%==C goto end
if %dropbackflag%==c goto end
if %dropbackflag%==1 goto installbsjj
if %dropbackflag%==2 goto installbsxt
if %dropbackflag%==3 goto installcsjj
if %dropbackflag%==4 goto installcsxt
goto end


:installbsjj
echo.
echo ************************************************************
echo *                                                          *
echo *                                                          *
echo *             正在升级:BS基金                                 *
echo *                                                          *
echo *                                                          *
echo ************************************************************
sqlplus %hsconuser%/%hsconpwd%@%tnsname% @.\Installbsjj.sql 
type .\log\install.log | find /i /n "ora-" > .\log\install.txt
type .\log\install.log | find /i /n "警告" >> .\log\install.txt
type .\log\install.log | find /i /n "SP2" >> .\log\install.txt
echo.
type .\log\install.txt
find /v "" /c  .\log\install.txt

:installbsxt
echo.
echo ************************************************************
echo *                                                          *
echo *                                                          *
echo *             正在升级:BS信托                                *
echo *                                                          *
echo *                                                          *
echo ************************************************************
sqlplus %hsconuser%/%hsconpwd%@%tnsname% @.\Installbsxt.sql 
type .\log\install.log | find /i /n "ora-" > .\log\install.txt
type .\log\install.log | find /i /n "警告" >> .\log\install.txt
type .\log\install.log | find /i /n "SP2" >> .\log\install.txt
echo.
type .\log\install.txt
find /v "" /c  .\log\install.txt

:installcsjj
echo.
echo ************************************************************
echo *                                                          *
echo *                                                          *
echo *             正在升级:cS基金                                 *
echo *                                                          *
echo *                                                          *
echo ************************************************************
sqlplus %hsconuser%/%hsconpwd%@%tnsname% @.\Installcsjj.sql 
type .\log\install.log | find /i /n "ora-" > .\log\install.txt
type .\log\install.log | find /i /n "警告" >> .\log\install.txt
type .\log\install.log | find /i /n "SP2" >> .\log\install.txt
echo.
type .\log\install.txt
find /v "" /c  .\log\install.txt

if %errorlevel% == 0 (
echo.
echo ************************************************************
echo *                                                         	*
echo *        升级完毕，但出现错误，请查看上面错误信息          	    *
echo *                                                          *
echo ************************************************************
echo.
goto end
) else (
echo.
echo ************************************************************
echo *                                                          *
echo *                         升级成功                    	    *
echo *                                                          *
echo ************************************************************
echo.
goto finsh
)
:finsh
echo.
echo ************************************************************
echo *                                                           	*
echo *                                                           	*
echo *             恒生反洗钱4.1主干升级完毕    	                    *
echo *                                                           	*
echo *                                                           	*
echo ************************************************************
echo.
goto end
:end
echo 按任意键退出
pause > nul
    