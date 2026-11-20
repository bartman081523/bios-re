/*
 * Module: SecSMIFlash
 * GUID: 3370a4bd-8c23-4565-a2a2-065feede6080
 * Source: /run/media/julian/ML6/bios-re/extracted/fid_rea/flash/FV@0x92f000/FFS-9e21fd93-9c72-4c15-8c4b-e77f1db2d792@0xa1ee78/section-0/section-1/FV@0x10/FFS-3370a4bd-8c23-4565-a2a2-065feede6080@0x859020/section-1.payload.bin
 */


// --- Procedure: 0x1300 ---

longlong entry(ulonglong param_1,longlong param_2)

{
  longlong lVar1;
  
  FUN_00001388(param_1,param_2);
  DAT_00006ad0 = -0x7fffffffffffffff;
  lVar1 = FUN_00001000((undefined8 *)&DAT_000069d0);
  if (lVar1 == 0) {
    lVar1 = FUN_000027e0(param_1,param_2);
    if ((-1 < lVar1) || (DAT_00006ad0 < 0)) {
      DAT_00006ad0 = lVar1;
    }
    FUN_000010d0(0x69d0,0xffffffffffffffff);
  }
  lVar1 = DAT_00006ad0;
  if (DAT_00006ad0 < 0) {
    FUN_000033e8();
  }
  return lVar1;
}




// --- Procedure: 0x2cd8 ---

undefined8 FUN_00002cd8(longlong param_1,longlong param_2,ulonglong param_3,undefined8 param_4)

{
  longlong lVar1;
  ulonglong *puVar2;
  uint uVar3;
  longlong lVar4;
  longlong lVar5;
  undefined8 uVar6;
  uint *puVar7;
  ulonglong uVar8;
  ulonglong uVar9;
  ulonglong uVar10;
  ulonglong uVar11;
  ulonglong uVar12;
  longlong lVar13;
  ulonglong *puVar14;
  
  lVar4 = DAT_00006908;
  uVar10 = 0;
  lVar1 = param_1 + (ulonglong)*(ushort *)(param_1 + 0x1e);
  uVar8 = (ulonglong)
          (longlong)(int)((uint)*(ushort *)(param_1 + 0x1c) - (uint)*(ushort *)(param_1 + 0x1e)) /
          0x18;
  if (uVar8 != 0) {
    puVar7 = (uint *)(lVar1 + 0x14);
    lVar13 = 0;
    do {
      lVar5 = lVar13;
      if (puVar7[-2] == 0) break;
      uVar3 = *puVar7;
      puVar7 = puVar7 + 6;
      uVar10 = uVar10 + 1;
      lVar5 = lVar13 + 1;
      if ((uVar3 & 0x200) == 0) {
        lVar5 = lVar13;
      }
      lVar13 = lVar5;
    } while (uVar10 < uVar8);
    if (lVar5 != 0) {
      uVar11 = lVar5 + 2;
      uVar8 = 0;
      uVar12 = 0;
      puVar2 = (ulonglong *)(DAT_00006908 + uVar11 * 8);
      if (uVar10 != 0) {
        puVar7 = (uint *)(lVar1 + 8);
        lVar13 = DAT_00006908 - (longlong)puVar2;
        puVar14 = puVar2;
        do {
          if (uVar11 <= uVar8) {
            return 0x800000000000001a;
          }
          if (puVar7[1] == 0) break;
          if ((puVar7[3] & 0x200) != 0) {
            uVar9 = (ulonglong)*puVar7;
            if (param_3 < uVar9) {
              return 0x800000000000001a;
            }
            if (param_3 < puVar7[1] + uVar9) {
              return 0x800000000000001a;
            }
            uVar8 = uVar8 + 1;
            *(ulonglong *)(lVar13 + (longlong)puVar14) = uVar9 + param_2;
            *puVar14 = (ulonglong)puVar7[1];
            puVar14 = puVar14 + 1;
          }
          uVar12 = uVar12 + 1;
          puVar7 = puVar7 + 6;
        } while (uVar12 < uVar10);
      }
      if (uVar8 < uVar11) {
        if ((*(byte *)(param_1 + 0x14) & 2) != 0) {
          *(longlong *)(lVar4 + uVar8 * 8) = param_1;
          puVar2[uVar8] = 0x38;
          uVar8 = uVar8 + 1;
          if (uVar11 <= uVar8) {
            return 0x800000000000001a;
          }
        }
        *(longlong *)(lVar4 + uVar8 * 8) = lVar1;
        puVar2[uVar8] = (uVar12 + 1) * 0x18;
        uVar6 = (**(code **)(DAT_00006b80 + 0x10))
                          (DAT_00006b80,param_4,uVar8 + 1,lVar4,puVar2,&DAT_00006b40);
        return uVar6;
      }
    }
  }
  return 0x800000000000001a;
}




// --- Procedure: 0x2024 ---

undefined8 FUN_00002024(char *param_1,ulonglong param_2,longlong *param_3)

{
  uint uVar1;
  undefined8 uVar2;
  longlong extraout_RAX;
  char *pcVar3;
  ulonglong *puVar4;
  undefined8 local_res20;
  
  local_res20 = 0;
  puVar4 = DAT_00006900;
  if (DAT_00006900 == (ulonglong *)0x0) {
LAB_00002052:
    uVar2 = FUN_00001e58((ulonglong)param_1,param_2,param_3);
  }
  else {
    while (*(int *)((longlong)puVar4 + 0xc) != 0) {
      if (param_1 < (char *)*puVar4) {
LAB_00002074:
        if ((char *)*puVar4 < param_1 + param_2) {
LAB_000020a2:
          if (((DAT_00006ad8 == 0x12) || (DAT_00006ad8 == 0x20)) ||
             (((uVar1 = *(uint *)((longlong)puVar4 + 0x14) & 0x400, uVar1 == 0 ||
               ((DAT_000061a1 & 4) != 0)) && ((uVar1 != 0 || ((DAT_000061a0 & 4) != 0)))))) {
            if ((*(uint *)((longlong)puVar4 + 0x14) & 0x200) == 0) {
              if (DAT_00006920 == '\0') {
                pcVar3 = param_1;
                if ((char *)0xff00102c < param_1) {
                  pcVar3 = param_1 + -0x102c;
                }
                if ((pcVar3 != (char *)0x0) &&
                   (param_1 = (char *)FUN_00002b84(pcVar3,(int)param_2 + 0x1000,&local_res20),
                   -1 < extraout_RAX)) {
                  *(uint *)((longlong)puVar4 + 0x14) = *(uint *)((longlong)puVar4 + 0x14) | 0x200;
                  DAT_00006920 = '\x01';
                  goto LAB_0000211d;
                }
              }
              if (DAT_00006918 == 0) {
                return 0;
              }
            }
LAB_0000211d:
            if (*(int *)((longlong)puVar4 + 0xc) != 0) goto LAB_00002052;
          }
          break;
        }
      }
      else {
        if (param_1 < (char *)((ulonglong)*(uint *)((longlong)puVar4 + 0xc) + *puVar4))
        goto LAB_000020a2;
        if (param_1 <= (char *)*puVar4) goto LAB_00002074;
      }
      puVar4 = puVar4 + 3;
      if (puVar4 == (ulonglong *)0x0) break;
    }
    uVar2 = 0x8000000000000008;
  }
  return uVar2;
}




// --- Procedure: 0x2900 ---

ulonglong FUN_00002900(longlong param_1)

{
  char cVar1;
  longlong lVar2;
  ulonglong uVar3;
  char *pcVar4;
  ulonglong uVar5;
  ulonglong uVar6;
  
  lVar2 = FUN_000048d8((longlong *)s_8ARNR302_00006348,(longlong *)(param_1 + 7),8);
  uVar3 = 0;
  if (lVar2 == 0) {
    pcVar4 = (char *)(param_1 + 0x26);
    uVar6 = uVar3;
    while( true ) {
      cVar1 = *pcVar4;
      if ((cVar1 < '0') || ('9' < cVar1)) break;
      pcVar4 = pcVar4 + 1;
      uVar6 = (ulonglong)(uint)((int)cVar1 + ((int)uVar6 * 5 + -0x18) * 2);
    }
    pcVar4 = (char *)(param_1 + 0x29);
    uVar5 = uVar3;
    while( true ) {
      cVar1 = *pcVar4;
      if ((cVar1 < '0') || ('9' < cVar1)) break;
      pcVar4 = pcVar4 + 1;
      uVar5 = (ulonglong)(uint)((int)cVar1 + ((int)uVar5 * 5 + -0x18) * 2);
    }
    if ((int)uVar6 * 100 + (int)uVar5 < 0x388) {
      uVar3 = 0x8000000000000019;
    }
  }
  else {
    uVar3 = 0x800000000000001a;
  }
  return uVar3;
}



