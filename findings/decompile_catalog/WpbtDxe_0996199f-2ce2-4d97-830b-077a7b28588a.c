/*
 * Module: WpbtDxe
 * GUID: 0996199f-2ce2-4d97-830b-077a7b28588a
 * Source: /run/media/julian/ML6/bios-re/extracted/fid_rea/flash/FV@0x92f000/FFS-9e21fd93-9c72-4c15-8c4b-e77f1db2d792@0xa1ee78/section-0/section-1/FV@0x10/FFS-0996199f-2ce2-4d97-830b-077a7b28588a@0x525508/section-1.payload.bin
 */


// --- Procedure: 0x2e0 ---

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void entry(undefined8 param_1,longlong param_2)

{
  undefined8 local_res8 [4];
  
  DAT_00000988 = *(undefined8 *)(param_2 + 0x60);
  if (DAT_000009a0 == 0) {
    DAT_00000990 = *(longlong *)(param_2 + 0x60);
    DAT_00000998 = *(undefined8 *)(param_2 + 0x58);
    DAT_000009a0 = param_2;
  }
  _DAT_00000980 = param_2;
  local_res8[0] = param_1;
  (**(code **)(DAT_00000990 + 0x170))(0x200,0x10,0x688,0,0x930,local_res8);
  return;
}




// --- Procedure: 0x478 ---

longlong FUN_00000478(void)

{
  short *psVar1;
  undefined4 uVar2;
  undefined2 uVar3;
  undefined4 uVar4;
  undefined2 uVar5;
  longlong lVar6;
  short *psVar7;
  longlong lVar8;
  short *psVar9;
  short *psVar10;
  longlong lVar11;
  undefined1 local_res8 [8];
  undefined8 local_res10;
  undefined8 local_res18;
  undefined8 *local_res20;
  undefined8 local_2d8;
  undefined4 *local_2d0;
  undefined8 local_2c8 [2];
  undefined1 local_2b8 [612];
  char local_54;
  
  psVar9 = (short *)0x0;
  local_2d8 = 0x282;
  local_res20 = (undefined8 *)0x0;
  local_2c8[0] = 0;
  local_res18 = 0;
  local_res10 = 0;
  lVar8 = (**(code **)(DAT_00000998 + 0x48))(0x950,0x900,local_res8,&local_2d8,local_2b8);
  if (-1 < lVar8) {
    if (local_54 == '\0') {
      lVar8 = -0x7ffffffffffffffd;
    }
    else {
      lVar8 = (**(code **)(DAT_00000990 + 0x140))(0x8f0,0,&local_res20);
      if (-1 < lVar8) {
        FUN_00000360(&local_res18,&local_res10);
        lVar6 = local_res10;
        lVar11 = (ulonglong)((local_res10 + 0x34 & 0xfff) != 0) + (local_res10 + 0x34 >> 0xc);
        lVar8 = (**(code **)(DAT_00000990 + 0x28))(0,9,lVar11,&local_2d0);
        if (-1 < lVar8) {
          lVar11 = lVar11 * 0x1000;
          (**(code **)(DAT_00000990 + 0x168))(local_2d0,lVar11);
          uVar5 = DAT_0000094c;
          uVar4 = DAT_00000948;
          uVar3 = DAT_00000944;
          uVar2 = DAT_00000940;
          local_2d0[1] = (int)lVar11;
          psVar1 = (short *)(local_2d0 + 0xd);
          *local_2d0 = 0x54425057;
          *(undefined2 *)(local_2d0 + 2) = 1;
          *(undefined2 *)((longlong)local_2d0 + 0xe) = uVar3;
          *(undefined4 *)((longlong)local_2d0 + 10) = uVar2;
          local_res10 = (ulonglong)CONCAT24(uVar5,uVar4);
          *(ulonglong *)(local_2d0 + 4) = local_res10;
          local_2d0[6] = 1;
          local_2d0[7] = 0x20544247;
          local_2d0[8] = 0x25021100;
          *(undefined2 *)((longlong)local_2d0 + 0x32) = 0;
          psVar7 = psVar9;
          do {
            psVar10 = psVar7;
            psVar9 = psVar9 + 1;
            psVar7 = (short *)((longlong)psVar10 + 1);
          } while (*psVar9 != 0);
          FUN_000006e0(psVar1,(ulonglong)(psVar10 + 1),(short *)0x0);
          (**(code **)(DAT_00000990 + 0x160))(psVar1,local_res18,lVar6);
          local_2d0[9] = (int)lVar6;
          local_2d0[1] = 0x34;
          *(short **)(local_2d0 + 10) = psVar1;
          *(undefined2 *)(local_2d0 + 0xc) = 0x101;
          lVar8 = (*(code *)*local_res20)(local_res20,local_2d0,0x34,local_2c8);
        }
      }
    }
  }
  return lVar8;
}




// --- Procedure: 0x688 ---

void FUN_00000688(undefined8 param_1)

{
  FUN_00000478();
                    /* WARNING: Could not recover jumptable at 0x000006a5. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(DAT_00000988 + 0x70))(param_1);
  return;
}



