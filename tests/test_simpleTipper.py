'''
@author Fabio Zadrozny
'''
import sys
import os

try:
    import __builtin__ #@UnusedImport
    BUILTIN_MOD = '__builtin__'
except ImportError:
    BUILTIN_MOD = 'builtins'


if sys.platform.find('java') == -1:

    HAS_WX = False

    import unittest
    try:
        from _pydev_bundle import _pydev_imports_tipper
    except:
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from _pydev_bundle import _pydev_imports_tipper
    import inspect

    class Test(unittest.TestCase):

        def p(self, t):
            for a in t:
                sys.stdout.write('%s\n' % (a,))

        def test_imports3(self):
            tip = _pydev_imports_tipper.generate_tip('os')
            ret = self.assertIn('path', tip)
            self.assertEquals('', ret[2])

        def test_imports2(self):
            try:
                tip = _pydev_imports_tipper.generate_tip('OpenGL.GLUT')
                self.assertIn('glutDisplayFunc', tip)
                self.assertIn('glutInitDisplayMode', tip)
            except ImportError:
                pass

        def test_imports4(self):
            try:
                tip = _pydev_imports_tipper.generate_tip('mx.DateTime.mxDateTime.mxDateTime')
                self.assertIn('now', tip)
            except ImportError:
                pass

        def test_imports5(self):
            tip = _pydev_imports_tipper.generate_tip('%s.list' % BUILTIN_MOD)
            s = self.assertIn('sort', tip)
            self.check_args(
                s,
                '(cmp=None, key=None, reverse=False)',
                '(self, object cmp, object key, bool reverse)',
                '(self, cmp: object, key: object, reverse: bool)',
                '(key=None, reverse=False)',
            )

        def test_imports2a(self):
            tips = _pydev_imports_tipper.generate_tip('%s.RuntimeError' % BUILTIN_MOD)
            self.assertIn('__doc__', tips)

        def test_imports2b(self):
            try:
                file
            except:
                pass
            else:
                tips = _pydev_imports_tipper.generate_tip('%s' % BUILTIN_MOD)
                t = self.assertIn('file' , tips)
                self.assert_('->' in t[1].strip() or 'file' in t[1])

        def test_imports2c(self):
            try:
                file # file is not available on py 3
            except:
                pass
            else:
                tips = _pydev_imports_tipper.generate_tip('%s.file' % BUILTIN_MOD)
                t = self.assertIn('readlines' , tips)
                self.assert_('->' in t[1] or 'sizehint' in t[1])

        def test_imports(self):
            '''
            You can print_ the results to check...
            '''
            if HAS_WX:
                tip = _pydev_imports_tipper.generate_tip('wxPython.wx')
                self.assertIn('wxApp'        , tip)

                tip = _pydev_imports_tipper.generate_tip('wxPython.wx.wxApp')

                try:
                    tip = _pydev_imports_tipper.generate_tip('qt')
                    self.assertIn('QWidget'        , tip)
                    self.assertIn('QDialog'        , tip)

                    tip = _pydev_imports_tipper.generate_tip('qt.QWidget')
                    self.assertIn('rect'           , tip)
                    self.assertIn('rect'           , tip)
                    self.assertIn('AltButton'      , tip)

                    tip = _pydev_imports_tipper.generate_tip('qt.QWidget.AltButton')
                    self.assertIn('__xor__'      , tip)

                    tip = _pydev_imports_tipper.generate_tip('qt.QWidget.AltButton.__xor__')
                    self.assertIn('__class__'      , tip)
                except ImportError:
                    pass

            tip = _pydev_imports_tipper.generate_tip(BUILTIN_MOD)
    #        for t in tip[1]:
    #            print_ t
            self.assertIn('object'         , tip)
            self.assertIn('tuple'          , tip)
            self.assertIn('list'          , tip)
            self.assertIn('RuntimeError'   , tip)
            self.assertIn('RuntimeWarning' , tip)

            # Remove cmp as it's not available on py 3
            #t = self.assertIn('cmp' , tip)
            #self.check_args(t, '(x, y)', '(object x, object y)', '(x: object, y: object)') #args

            t = self.assertIn('isinstance' , tip)
            self.check_args(t, '(object, class_or_type_or_tuple)', '(object o, type typeinfo)', '(o: object, typeinfo: type)') #args

            t = self.assertIn('compile' , tip)
            self.check_args(t, '(source, filename, mode)', '()', '(o: object, name: str, val: object)') #args

            t = self.assertIn('setattr' , tip)
            self.check_args(t, '(object, name, value)', '(object o, str name, object val)', '(o: object, name: str, val: object)') #args

            try:
                import compiler
                compiler_module = 'compiler'
            except ImportError:
                try:
                    import ast
                    compiler_module = 'ast'
                except ImportError:
                    compiler_module = None

            if compiler_module is not None: #Not available in iron python
                tip = _pydev_imports_tipper.generate_tip(compiler_module)
                if compiler_module == 'compiler':
                    self.assertArgs('parse', '(buf, mode)', tip)
                    self.assertArgs('walk', '(tree, visitor, walker, verbose)', tip)
                    self.assertIn('parseFile'      , tip)
                else:
                    self.assertArgs('parse', '(source, filename, mode)', tip)
                    self.assertArgs('walk', '(node)', tip)
                self.assertIn('parse'          , tip)


        def check_args(self, t, *expected):
            for x in expected:
                if x == t[2]:
                    return
            self.fail('Found: %s. Expected: %s' % (t[2], expected))


        def assertArgs(self, tok, args, tips):
            for a in tips[1]:
                if tok == a[0]:
                    self.assertEquals(args, a[2])
                    return
            raise AssertionError('%s not in %s', tok, tips)

        def assertIn(self, tok, tips):
            for a in tips[1]:
                if tok == a[0]:
                    return a
            raise AssertionError('%s not in %s' % (tok, tips))


        def test_search(self):
            s = _pydev_imports_tipper.Search('inspect.ismodule')
            (f, line, col), foundAs = s
            self.assert_(line > 0)


        def test_dot_net_libraries(self):
            if sys.platform == 'cli':
                tip = _pydev_imports_tipper.generate_tip('System.Drawing')
                self.assertIn('Brushes' , tip)

                tip = _pydev_imports_tipper.generate_tip('System.Drawing.Brushes')
                self.assertIn('Aqua' , tip)


        def test_inspect(self):

            class C(object):
                def metA(self, a, b):
                    pass

            obj = C.metA
            if inspect.ismethod (obj):
                pass
    #            print_ obj.im_func
    #            print_ inspect.getargspec(obj.im_func)


    def suite():
        s = unittest.TestSuite()
        s.addTest(Test("test_imports5"))
        unittest.TextTestRunner(verbosity=2).run(s)


if __name__ == '__main__':
    if sys.platform.find('java') == -1:
#        suite()
        unittest.main()
    else:
        sys.stdout.write('Not running python tests in platform: %s\n' % (sys.platform,))

