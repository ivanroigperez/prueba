' ==========================================================================
'  Macro SOLIDWORKS - Ensamblajes del taburete-escalera
'  Crea C:\Taburete\Taburete_abierto.SLDASM y C:\Taburete\Taburete_plegado.SLDASM
'  con las piezas colocadas (posición calculada en el estudio cinemático) y
'  3 configuraciones que usan ALT1_ACERO, ALT2_ALUMINIO y ALT3_MADERA.
'  Escribe C:\Taburete\masas_conjunto.csv con la masa total de cada alternativa.
' ==========================================================================
Option Explicit
Const CARPETA As String = "C:\Taburete\"
Dim swApp As Object
Dim Assy As Object
Dim mu As Object
Dim componentes As Collection
Dim informe As String
Dim csv As String

Sub Poner(nombre As String, m)
    ' m = 9 términos de rotación (ejes X, Y, Z de la pieza) + 3 de traslación en metros
    Dim comp As Object, d(15) As Double, i As Integer, tr As Object
    Set comp = Assy.AddComponent5(CARPETA & nombre & ".SLDPRT", 0, "", False, "", 0, 0, 0)
    If comp Is Nothing Then
        informe = informe & "  ERROR al insertar " & nombre & vbCrLf
        Exit Sub
    End If
    For i = 0 To 11: d(i) = m(i): Next i
    d(12) = 1#
    Set tr = mu.CreateTransform((d))
    comp.Transform2 = tr
    componentes.Add comp
End Sub

Sub AbrirPiezas()
    Dim n, errs As Long, warns As Long
    For Each n In Array("Larguero_delantero", "Pata_trasera", "Travesano_asidero", "Travesano_trasero", _
                        "Plataforma", "Peldano", "Biela_plataforma", "Tirante_peldano")
        swApp.OpenDoc6 CARPETA & n & ".SLDPRT", 1, 1, "", errs, warns
    Next n
End Sub

Sub Crear(nombre As String, plegado As Boolean)
    Dim plantilla As String, c, cfg, k As Integer, errs As Long, warns As Long, mp As Object, fila As String
    plantilla = swApp.GetUserPreferenceStringValue(9)
    Set Assy = swApp.NewDocument(plantilla, 0, 0, 0)
    If Assy Is Nothing Then MsgBox "No se pudo crear el ensamblaje (plantilla).", vbCritical: End
    Set componentes = New Collection
    If plegado Then
'@@PLEGADO@@
    Else
'@@ABIERTO@@
    End If
    ' fijar todos los componentes en su posición
    Assy.ClearSelection2 True
    For Each c In componentes
        c.Select4 True, Nothing, False
    Next c
    Assy.FixComponent
    Assy.ClearSelection2 True
    ' configuraciones por alternativa de material
    Assy.GetActiveConfiguration.Name = "ALT2_ALUMINIO"
    Assy.AddConfiguration3 "ALT1_ACERO", "Alternativa 1: acero", "", 0
    Assy.AddConfiguration3 "ALT3_MADERA", "Alternativa 3: madera", "", 0
    fila = nombre
    For Each cfg In Array("ALT1_ACERO", "ALT2_ALUMINIO", "ALT3_MADERA")
        Assy.ShowConfiguration2 cfg
        For Each c In componentes
            c.ReferencedConfiguration = cfg
        Next c
        Assy.EditRebuild3
        Set mp = Assy.Extension.CreateMassProperty
        If mp Is Nothing Then fila = fila & ";" Else fila = fila & ";" & Format(mp.Mass, "0.000")
    Next cfg
    Assy.ShowConfiguration2 "ALT2_ALUMINIO"
    Assy.EditRebuild3
    Assy.ShowNamedView2 "", 7
    Assy.ViewZoomtofit2
    csv = csv & fila & vbCrLf
    Assy.Extension.SaveAs CARPETA & nombre & ".SLDASM", 0, 1, Nothing, errs, warns
    If errs <> 0 Then informe = informe & "  ERROR al guardar " & nombre & vbCrLf
    informe = informe & "OK  " & nombre & " (" & componentes.Count & " componentes)" & vbCrLf
End Sub

Sub main()
    Set swApp = Application.SldWorks
    Set mu = swApp.GetMathUtility
    csv = "Ensamblaje;Masa ALT1_ACERO (kg);Masa ALT2_ALUMINIO (kg);Masa ALT3_MADERA (kg)" & vbCrLf
    AbrirPiezas
    Crear "Taburete_plegado", True
    swApp.CloseDoc Assy.GetTitle
    Crear "Taburete_abierto", False
    Dim f As Integer: f = FreeFile
    Open CARPETA & "masas_conjunto.csv" For Output As #f
    Print #f, csv
    Close #f
    MsgBox "Ensamblajes creados." & vbCrLf & vbCrLf & informe & vbCrLf & _
           "Masas totales en " & CARPETA & "masas_conjunto.csv", vbInformation, "Taburete"
End Sub
