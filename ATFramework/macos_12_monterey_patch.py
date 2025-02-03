import re
import objc
from objc import getClassList
from .utils.log import logger

def monterey_patch(self):
    try:
        if not monterey_patch.enable_monerey_patch: logger("Monterey Patch is failed")
    except:
        monterey_patch.enable_monerey_patch = True
        logger("Monterey Patch is enabled")

    # Ensure that all dynamic entries get loaded
    if self.__varmap_dct:
        dct = {}
        objc.loadBundleVariables(
            self.__bundle,
            dct,
            [
                (nm, self.__varmap_dct[nm].encode("ascii"))
                for nm in self.__varmap_dct
                if not self.__varmap_dct[nm].startswith("=")
            ],
        )
        for nm in dct:
            if nm not in self.__dict__:
                self.__dict__[nm] = dct[nm]

        for nm, tp in self.__varmap_dct.items():
            if tp.startswith("=="):
                try:
                    self.__dict__[nm] = objc._loadConstant(nm, tp[2:], 2)
                except AttributeError:
                    raise
                    pass
            elif tp.startswith("="):
                try:
                    self.__dict__[nm] = objc._loadConstant(nm, tp[1:], 1)
                except AttributeError:
                    pass

        self.__varmap_dct = {}

    if self.__varmap:
        varmap = []
        specials = []
        for nm, tp in re.findall(
                r"\$([A-Z0-9a-z_]*)(@[^$]*)?(?=\$)", self.__varmap
        ):
            if tp and tp.startswith("@="):
                specials.append((nm, tp[2:]))
            else:
                varmap.append((nm, b"@" if not tp else tp[1:].encode("ascii")))

        dct = {}
        objc.loadBundleVariables(self.__bundle, dct, varmap)

        for nm in dct:
            if nm not in self.__dict__:
                self.__dict__[nm] = dct[nm]

        for nm, tp in specials:
            try:
                if tp.startswith("="):
                    self.__dict__[nm] = objc._loadConstant(nm, tp[1:], 2)
                else:
                    self.__dict__[nm] = objc._loadConstant(nm, tp, 1)
            except AttributeError:
                pass

        self.__varmap = ""

    if self.__enummap:
        for nm, val in re.findall(
                r"\$([A-Z0-9a-z_]*)@([^$]*)(?=\$)", self.__enummap
        ):
            if nm not in self.__dict__:
                self.__dict__[nm] = self.__prs_enum(val)

        self.__enummap = ""

    if self.__funcmap:
        func_list = []
        for nm in self.__funcmap:
            if nm not in self.__dict__:
                func_list.append((nm,) + self.__funcmap[nm])

        dct = {}
        objc.loadBundleFunctions(self.__bundle, dct, func_list)
        for nm in dct:
            if nm not in self.__dict__:
                self.__dict__[nm] = dct[nm]

        if self.__inlinelist is not None:
            dct = {}
            objc.loadFunctionList(
                self.__inlinelist, dct, func_list, skip_undefined=True
            )
            for nm in dct:
                if nm not in self.__dict__:
                    self.__dict__[nm] = dct[nm]

        self.__funcmap = {}

    if self.__expressions:
        for nm in list(self.__expressions):
            try:
                getattr(self, nm)
            except AttributeError:
                pass

    if self.__aliases:
        for nm in list(self.__aliases):
            try:
                getattr(self, nm)
            except AttributeError:
                pass

    all_names = set()

    # Add all names that are already in our __dict__
    all_names.update(self.__dict__)

    # Merge __all__of parents ('from parent import *')
    for p in self.__parents:
        try:
            all_names.update(p.__all__)
        except AttributeError:
            all_names.update(dir(p))

    # Add all class names
    all_names.update(cls.__name__ for cls in getClassList() if "." not in cls.__name__)

    return [v for v in all_names if not v.startswith("_")]
objc.ObjCLazyModule._ObjCLazyModule__calc_all = monterey_patch

